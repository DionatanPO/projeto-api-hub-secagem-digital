# Projeto HUB Secagem Digital 🚀

Este repositório contém o backend do **HUB Secagem Digital**, uma plataforma centralizada para monitoramento de infraestrutura de servidores e gerenciamento de projetos. Desenvolvido com Django e Django REST Framework, o sistema permite o controle remoto de serviços e o acompanhamento detalhado de estatísticas de servidor via SSH.

## 📋 Funcionalidades Principais

### 🖥️ Gestão de Infraestrutura (via SSH)
- **Monitoramento em Tempo Real:** Visualização de uso de CPU, Memória RAM, Disco e Uptime.
- **Controle de Serviços:** Interface para iniciar, parar e reiniciar serviços uWSGI/Systemd de sites gerenciados.
- **Exploração de Logs:** Acesso rápido aos logs do sistema (`syslog`) para depuração.
- **Status de Domínios:** Verificação automática de status HTTP (Online/Offline) para domínios configurados no servidor.
- **Processos do Sistema:** Listagem dos processos que mais consomem recursos.

### 📂 Gerenciamento de Projetos
- **CRUD de Projetos:** Cadastro e acompanhamento de projetos com suporte a diferentes estados (Prospecção, Planejamento, Desenvolvimento, Manutenção, Finalizado, Pausado).
- **Dados Detalhados:** Registro de clientes, datas de início, descrições e observações técnicas.

### 🔐 Segurança e Acessos
- **Autenticação:** Baseada em Tokens (DRF Token Authentication).
- **Níveis de Acesso:**
  - **ADMIN:** Acesso total, incluindo execução de comandos de gerenciamento de serviços.
  - **EQUIPE:** Acesso para visualização de estatísticas, processos e projetos.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** [Django 6.0](https://www.djangoproject.com/)
- **API:** [Django REST Framework](https://www.django-rest-framework.org/)
- **Banco de Dados:** SQLite (Desenvolvimento)
- **Comunicação SSH:** [Paramiko](https://www.paramiko.org/)
- **Ambiente:** Python 3.x
- **Integração:** CORS configurado para consumo por aplicações Frontend (Web/Flutter).

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10+
- Pip (Gerenciador de pacotes)
- Virtualenv (Recomendado)

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/projeto-hub-secagem-digital.git
   cd projeto-hub-secagem-digital
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows:
   .\venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Nota: Caso não tenha o arquivo requirements.txt, instale: `django djangorestframework django-cors-headers paramiko python-dotenv requests`)*

4. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:
   ```env
   SSH_HOST=seu_ip_ou_host
   SSH_USERNAME=seu_usuario
   SSH_PASSWORD=sua_senha
   SSH_PORT=22
   ```

5. **Execute as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```

6. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

---

## 🛣️ Endpoints Principais (API)

| Método | Endpoint | Descrição | Permissão |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/infra/status/` | Estatísticas de CPU/RAM/Disco | Equipe |
| `GET` | `/api/infra/processes/` | Top processos do servidor | Equipe |
| `GET` | `/api/infra/domains/` | Lista sites e status HTTP | Equipe |
| `POST` | `/api/infra/manage/` | Iniciar/Reiniciar serviços | Admin |
| `GET` | `/api/projects/` | Lista todos os projetos | Equipe |

---

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).

---
*Desenvolvido para otimizar a operação técnica da Secagem Digital.*
