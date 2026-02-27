# Projeto HUB Secagem Digital 🚀

Este repositório contém o backend do **HUB Secagem Digital**, uma plataforma centralizada para monitoramento de infraestrutura de servidores e gerenciamento de projetos. Desenvolvido com Django e Django REST Framework, o sistema permite o controle remoto de serviços e o acompanhamento detalhado de estatísticas de servidor via SSH.

<img width="1920" height="1080" alt="Captura de Tela (96)" src="https://github.com/user-attachments/assets/6bccdd09-3ec2-4e93-90ae-f4cd4cc6c5fb" />


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


## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).

---
*Desenvolvido para otimizar a operação técnica da Secagem Digital.*
