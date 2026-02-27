import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

class SSHConnector:
    def __init__(self, host=None, username=None, password=None, port=22):
        self.host = host or os.getenv('SSH_HOST')
        self.username = username or os.getenv('SSH_USERNAME')
        self.password = password or os.getenv('SSH_PASSWORD')
        self.port = port or int(os.getenv('SSH_PORT', 22))
        self.client = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=10
            )
            return True, "Conexão estabelecida com sucesso."
        except Exception as e:
            return False, f"Erro ao conectar: {str(e)}"

    def execute_command(self, command):
        if not self.client:
            success, message = self.connect()
            if not success:
                return None, message, -1

        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_code = stdout.channel.recv_exit_status()
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            return output, error, exit_code
        except Exception as e:
            return None, f"Erro ao executar comando: {str(e)}", -1

    def get_system_stats(self):
        """
        Coleta estatísticas básicas do sistema via SSH.
        """
        commands = {
            "cpu": "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'",
            "memory": "free -m | awk 'NR==2{printf \"%.2f\", $3*100/$2}'",
            "disk": "df -h / | awk 'NR==2{print $5}' | sed 's/%//'",
            "uptime": "uptime -p",
            "load": "cat /proc/loadavg | awk '{print $1 \", \" $2 \", \" $3}'"
        }
        
        results = {}
        for key, cmd in commands.items():
            output, error, exit_code = self.execute_command(cmd)
            if output:
                results[key] = output.strip()
            else:
                results[key] = "N/A"
        
        return results

    def get_processes(self):
        """
        Lista os 10 processos que mais consomem CPU.
        """
        cmd = "ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 11"
        output, error, exit_code = self.execute_command(cmd)
        if output:
            lines = output.strip().split('\n')
            header = lines[0].split()
            processes = []
            for line in lines[1:]:
                parts = line.split(None, 4)
                if len(parts) >= 5:
                    processes.append({
                        "pid": parts[0],
                        "ppid": parts[1],
                        "mem": parts[3],
                        "cpu": parts[4],
                        "command": parts[2]
                    })
            return processes
        return []

    def get_logs(self, lines=50):
        """
        Obtém as últimas linhas do syslog.
        """
        cmd = f"tail -n {lines} /var/log/syslog"
        output, error, exit_code = self.execute_command(cmd)
        return output if output else error

    def get_network_stats(self):
        """
        Obtém estatísticas de rede (interfaces ativas).
        """
        cmd = "ip -brief addr"
        output, error, exit_code = self.execute_command(cmd)
        return output.strip() if output else "N/A"

    def get_domains(self):
        """
        Tenta listar domínios/sites e verifica se estão online.
        Refinado para tratar arquivos .conf e nomes de projetos Django.
        """
        import requests
        
        # Busca em locais comuns
        cmd = "ls /etc/nginx/sites-enabled /etc/apache2/sites-enabled /var/www /home -I html -I index.lighttpd.html -I venv -I .broken -I .bash* 2>/dev/null"
        output, error, exit_code = self.execute_command(cmd)
        
        domain_list = []
        if output:
            found_items = list(set([item for item in output.strip().split() if item]))
            
            processed_domains = set()
            for item in found_items:
                # 1. Limpeza do nome (remove .conf se houver)
                display_name = item
                clean_name = item
                if item.endswith('.conf'):
                    clean_name = item[:-5]
                
                # Ignorar arquivos genéricos ou de sistema
                if clean_name in ['default', '000-default', 'localhost']:
                    continue
                
                if clean_name in processed_domains:
                    continue
                processed_domains.add(clean_name)

                # 2. FILTRAGEM: Mostrar apenas se parecer um domínio (contém ponto)
                if "." not in clean_name:
                    continue

                # 3. Lógica de Status (HTTP)
                status = "unknown"
                url = f"http://{clean_name}"
                try:
                    # Timeout curto, ignora verificação SSL se for HTTPS
                    response = requests.get(url, timeout=3, allow_redirects=True)
                    if response.status_code < 400:
                        status = "online"
                    else:
                        status = "error_status"
                except:
                    status = "offline"

                domain_list.append({
                    "name": clean_name,
                    "original_file": item,
                    "status": status,
                    "url": url
                })
                
        return domain_list

    def manage_service(self, domain, action):
        """
        Gerencia o serviço systemd associado ao domínio (start, stop, restart).
        Assume o padrão: <domain>.uwsgi.service
        """
        valid_actions = ['start', 'stop', 'restart']
        if action not in valid_actions:
            return False, f"Ação '{action}' inválida."

        import re
        if not re.match(r'^[a-zA-Z0-9\.-]+$', domain):
            return None, "Nome de domínio inválido."

        service_name = f"{domain}.uwsgi.service"
        
        # Executa o comando principal
        cmd = f"systemctl {action} {service_name}"
        output, error, exit_code = self.execute_command(cmd)
        
        if exit_code != 0:
            return False, f"Erro ao executar {action}: {error or 'Comando retornou erro.'}"

        # Se for start ou restart, verificamos se o serviço ficou 'active (running)'
        if action in ['start', 'restart']:
            # Damos meio segundo para o uwsgi tentar subir
            import time
            time.sleep(0.5)
            
            status_cmd = f"systemctl is-active {service_name}"
            status_out, status_err, status_code = self.execute_command(status_cmd)
            
            # systemctl is-active retorna 'active' se ok, e exit_code 0.
            # Se falhou, retorna 'failed' ou 'inactive' e exit_code != 0
            if status_code != 0 or status_out.strip() != "active":
                # Se falhou, pegamos o motivo no journal
                log_cmd = f"journalctl -u {service_name} -n 5 --no-pager"
                log_out, _, _ = self.execute_command(log_cmd)
                return False, f"O serviço foi iniciado mas falhou logo em seguida. Motivo:\n{log_out}"

        return True, f"Serviço {service_name} executou '{action}' com sucesso."

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
