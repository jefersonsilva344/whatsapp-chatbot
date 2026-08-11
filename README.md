WhatsApp Chatbot

Chatbot automatizado para atendimento via WhatsApp Web, desenvolvido em Python com Selenium, SQLite e Pytest, utilizando arquitetura modular, gerenciamento de sessões, máquina de estados e integração com IA.

📌 Sobre o projeto

O WhatsApp Chatbot é uma aplicação de automação de atendimento desenvolvida em Python para interagir com o WhatsApp Web.

O projeto foi estruturado para ir além de uma simples automação com Selenium, utilizando separação de responsabilidades, persistência de dados, gerenciamento de sessões, controle de estados, processamento de mensagens e testes automatizados.

A aplicação foi desenvolvida com foco em arquitetura modular, testabilidade e facilidade de manutenção.

🚀 Funcionalidades
Automação do WhatsApp Web
Leitura de mensagens recebidas
Envio automático de respostas
Identificação e processamento de mensagens
Prevenção de mensagens duplicadas
Gerenciamento de conversas
Gerenciamento de sessões
Máquina de estados para controle do atendimento
Fluxos automatizados de atendimento
Persistência de mensagens e conversas em SQLite
Sistema de respostas baseado em regras e intenções
Normalização de mensagens
Integração com serviço de IA
Memória de contexto
Monitoramento de conversas
Injeção de dependências através de um container
Testes unitários
Testes de integração
🏗️ Arquitetura

O processamento principal segue aproximadamente o fluxo:

                    WhatsApp Web
                         │
                         ▼
                    WhatsAppBot
                         │
                         ▼
                      Monitor
                         │
                         ▼
                 MessageProcessor
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
      ConversationManager     MessageRepository
              │                     │
              ▼                     ▼
       SessionManager             SQLite
              │
              ▼
         StateManager
              │
              ▼
          FlowManager
              │
       ┌──────┴──────┐
       ▼             ▼
   Responder        IA
       │             │
       └──────┬──────┘
              ▼
           Resposta
              │
              ▼
        WhatsApp Web

Essa separação permite que cada componente tenha uma responsabilidade específica, facilitando manutenção, testes e evolução do sistema.

📂 Estrutura do projeto
whatsapp-chatbot/
│
├── src/
│   ├── bot/
│   │   ├── message_reader.py
│   │   ├── message_sender.py
│   │   ├── profile_manager.py
│   │   ├── search_manager.py
│   │   └── whatsapp_bot.py
│   │
│   ├── chat/
│   │   ├── chat_manager.py
│   │   ├── conversation.py
│   │   └── unread_detector.py
│   │
│   ├── conversation/
│   │   └── conversation_manager.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── conversation_repository.py
│   │   ├── mapper.py
│   │   ├── message_repository.py
│   │   └── migrations.py
│   │
│   ├── flow/
│   │   ├── flow_manager.py
│   │   └── flows.py
│   │
│   ├── ia/
│   │   ├── memoria.py
│   │   ├── openai_service.py
│   │   └── prompt.py
│   │
│   ├── message/
│   │   └── message_processor.py
│   │
│   ├── models/
│   │   ├── chat_message.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   └── session.py
│   │
│   ├── responder/
│   │   ├── intents.py
│   │   ├── normalizador.py
│   │   ├── regras.py
│   │   ├── responder.py
│   │   └── respostas.py
│   │
│   ├── session/
│   │   └── session_manager.py
│   │
│   ├── state/
│   │   ├── state_manager.py
│   │   └── states.py
│   │
│   ├── tests/
│   │   ├── test_container.py
│   │   ├── test_conversation_manager.py
│   │   ├── test_conversation_repository.py
│   │   ├── test_flow_manager.py
│   │   ├── test_integration.py
│   │   ├── test_main.py
│   │   ├── test_message_processor.py
│   │   ├── test_message_repository.py
│   │   ├── test_monitor.py
│   │   ├── test_openai.py
│   │   ├── test_session_manager.py
│   │   └── test_state_manager.py
│   │
│   ├── config.py
│   ├── container.py
│   ├── logger.py
│   ├── main.py
│   ├── monitor.py
│   ├── selector_manager.py
│   ├── selectors.py
│   └── utils.py
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
🔄 Fluxo de atendimento

O chatbot utiliza estados para controlar o andamento de uma conversa.

Exemplo de fluxo:

INICIO
   │
   ▼
AGUARDANDO_NOME
   │
   ▼
AGUARDANDO_SERVICO
   │
   ▼
ORCAMENTO
   │
   ▼
CONFIRMACAO
   │
   ▼
FINALIZADO

Cada etapa determina quais informações devem ser coletadas e qual será o próximo comportamento do chatbot.

🧠 Integração com IA

O projeto possui uma camada específica para integração com IA:

src/ia/
├── memoria.py
├── openai_service.py
└── prompt.py

Essa separação permite manter a integração com o serviço de IA isolada do restante da aplicação.

As credenciais devem ser configuradas através de variáveis de ambiente e não devem ser armazenadas no repositório.

🗄️ Persistência

O projeto utiliza SQLite para armazenamento local.

Entre os dados gerenciados estão:

Mensagens
Conversas
Histórico de atendimento
Informações relacionadas às sessões

Os bancos de dados locais são ignorados pelo Git através do .gitignore.

🧪 Testes

O projeto possui uma suíte de testes automatizados utilizando Pytest.

Foram implementados testes para diferentes componentes da aplicação, incluindo:

Container
Conversation Manager
Conversation Repository
Flow Manager
Message Processor
Message Repository
Monitor
Session Manager
State Manager
Integração
Serviço de IA
Executar os testes
python -m pytest -v

Resultado atual da suíte:

89 passed
🛠️ Tecnologias
Tecnologia	Utilização
Python	Linguagem principal
Selenium	Automação do WhatsApp Web
SQLite	Persistência local
Pytest	Testes automatizados
WebDriver Manager	Gerenciamento do ChromeDriver
OpenAI API	Integração com IA
⚙️ Instalação

Clone o repositório:

git clone https://github.com/SEU-USUARIO/whatsapp-chatbot.git
cd whatsapp-chatbot

Crie o ambiente virtual:

python -m venv venv
Windows
venv\Scripts\activate

Instale as dependências:

pip install -r requirements.txt
🔐 Configuração

Crie um arquivo .env local com as variáveis necessárias para a aplicação.

Exemplo:

OPENAI_API_KEY=sua_chave_aqui

Nunca publique chaves de API, tokens, credenciais, sessões do WhatsApp ou arquivos .env no GitHub.

▶️ Executando a aplicação

Com o ambiente virtual ativado:

python src/main.py

O chatbot iniciará a automação do WhatsApp Web utilizando Selenium.

Na primeira execução, será necessário realizar a autenticação no WhatsApp Web.

⚠️ Dados locais

Os seguintes arquivos e diretórios são utilizados localmente e não fazem parte do repositório:

venv/
.env
data/*.db
data/*.sqlite
data/chrome_profile/

O diretório chrome_profile pode armazenar informações da sessão do navegador e, consequentemente, dados de autenticação do WhatsApp.

Por segurança, ele deve permanecer fora do GitHub.

🎯 Objetivos técnicos

Este projeto foi desenvolvido com foco em:

Arquitetura modular
Separação de responsabilidades
Baixo acoplamento entre componentes
Persistência de dados
Gerenciamento de estado
Automação web
Integração com IA
Testes automatizados
Manutenibilidade
Evolução incremental da aplicação
📈 Possíveis evoluções

Algumas melhorias planejadas para futuras versões:

Dashboard para monitoramento
Sistema de métricas
Logs estruturados
Dockerização
Banco de dados externo
API REST
Sistema de autenticação
Filas para processamento de mensagens
Melhorias na camada de IA
Deploy em ambiente cloud
CI/CD com GitHub Actions
⚖️ Aviso

Este projeto foi desenvolvido para fins educacionais, experimentais e de portfólio.

A utilização de automações no WhatsApp deve respeitar os termos de uso da plataforma e as regras aplicáveis ao uso de mensagens automatizadas.

👨‍💻 Autor

Jeferson Silva

Projeto desenvolvido como parte do portfólio de desenvolvimento Python, automação e integração com IA.