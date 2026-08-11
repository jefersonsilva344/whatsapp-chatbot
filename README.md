# 🤖 WhatsApp Chatbot

Chatbot automatizado para atendimento via **WhatsApp Web**, desenvolvido em **Python**, utilizando **Selenium, SQLite, Pytest e integração com IA**.

O projeto utiliza uma arquitetura modular com gerenciamento de sessões, máquina de estados, processamento de mensagens, persistência de dados, automação web e testes automatizados.

[![Tests](https://github.com/jefersonsilva344/whatsapp-chatbot/actions/workflows/tests.yml/badge.svg)](https://github.com/jefersonsilva344/whatsapp-chatbot/actions)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-Automation-green?logo=selenium)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-89%20tests-orange?logo=pytest)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Sobre o projeto

O **WhatsApp Chatbot** é uma aplicação de automação de atendimento desenvolvida em Python para interagir com o WhatsApp Web.

O projeto foi estruturado para ir além de uma automação simples com Selenium, utilizando **separação de responsabilidades, injeção de dependências, persistência de dados, gerenciamento de sessões, máquina de estados, processamento de mensagens e testes automatizados**.

A arquitetura foi desenvolvida com foco em:

* Modularidade
* Baixo acoplamento
* Testabilidade
* Manutenibilidade
* Evolução incremental
* Separação de responsabilidades

---

## 🚀 Funcionalidades

### Automação

* Automação do WhatsApp Web
* Leitura de mensagens recebidas
* Envio automático de respostas
* Abertura de conversas
* Identificação do usuário logado
* Monitoramento de conversas

### Processamento

* Processamento de mensagens
* Normalização de conteúdo
* Identificação de intenções
* Prevenção de mensagens duplicadas
* Geração de respostas
* Histórico de atendimento

### Gerenciamento

* Gerenciamento de conversas
* Gerenciamento de sessões
* Máquina de estados
* Fluxos automatizados de atendimento
* Persistência de dados em SQLite

### Inteligência Artificial

* Integração com OpenAI API
* Camada de serviço dedicada para IA
* Memória de contexto
* Sistema de prompts
* Separação entre regras determinísticas e respostas baseadas em IA

### Qualidade

* Testes unitários
* Testes de integração
* Testes dos principais componentes
* Execução automatizada com Pytest
* CI utilizando GitHub Actions

---

# 🏗️ Arquitetura

O processamento principal da aplicação segue aproximadamente o seguinte fluxo:

```text
                    WhatsApp Web
                         │
                         ▼
                  ┌──────────────┐
                  │ WhatsAppBot  │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Monitor    │
                  └──────┬───────┘
                         │
                         ▼
               ┌──────────────────┐
               │ MessageProcessor │
               └────────┬─────────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
    ┌──────────────────┐   ┌──────────────────┐
    │ConversationManager│   │ MessageRepository│
    └─────────┬────────┘   └─────────┬────────┘
              │                      │
              ▼                      ▼
    ┌──────────────────┐          SQLite
    │ SessionManager   │
    └─────────┬────────┘
              │
              ▼
    ┌──────────────────┐
    │  StateManager    │
    └─────────┬────────┘
              │
              ▼
    ┌──────────────────┐
    │   FlowManager    │
    └─────────┬────────┘
              │
        ┌─────┴─────┐
        ▼           ▼
   ┌─────────┐  ┌──────────────┐
   │ Responder│  │ OpenAIService│
   └────┬────┘  └──────┬───────┘
        │              │
        └──────┬───────┘
               ▼
          Resposta
               │
               ▼
          WhatsApp Web
```

Essa separação permite que cada componente tenha uma responsabilidade específica, facilitando testes, manutenção e evolução da aplicação.

---

# 📂 Estrutura do projeto

```text
whatsapp-chatbot/
│
├── src/
│   │
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
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# 🔄 Fluxo de atendimento

O chatbot utiliza uma **máquina de estados** para controlar o andamento de cada conversa.

Exemplo de fluxo:

```text
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
```

Cada estado determina quais informações devem ser coletadas e qual será o próximo comportamento do chatbot.

Isso permite manter o contexto da conversa sem depender exclusivamente do conteúdo da última mensagem recebida.

---

# 🧠 Integração com IA

A aplicação possui uma camada específica para integração com serviços de inteligência artificial:

```text
src/ia/
├── memoria.py
├── openai_service.py
└── prompt.py
```

Essa separação mantém a integração com a IA desacoplada do restante da aplicação.

A aplicação também possui uma camada de resposta baseada em regras e intenções:

```text
src/responder/
├── intents.py
├── normalizador.py
├── regras.py
├── responder.py
└── respostas.py
```

Essa abordagem permite combinar **regras determinísticas** com **respostas geradas por IA**, dependendo do contexto da interação.

As credenciais são obtidas através de variáveis de ambiente e não são armazenadas no repositório.

---

# 🗄️ Persistência

O projeto utiliza **SQLite** para armazenamento local.

Entre os dados gerenciados estão:

* Mensagens
* Conversas
* Histórico de atendimento
* Informações relacionadas às sessões

A camada de persistência utiliza repositories para separar o acesso ao banco da lógica de negócio.

Exemplo:

```text
MessageProcessor
      │
      ▼
MessageRepository
      │
      ▼
SQLite
```

Os arquivos de banco de dados locais são ignorados pelo Git através do `.gitignore`.

---

# 🧪 Testes

O projeto possui uma suíte automatizada utilizando **Pytest**.

Os testes cobrem diferentes camadas da aplicação:

* Container
* Conversation Manager
* Conversation Repository
* Flow Manager
* Message Processor
* Message Repository
* Monitor
* Session Manager
* State Manager
* Integração
* Serviço de IA
* Fluxo completo de atendimento

### Executar os testes

```bash
python -m pytest -v
```

### Resultado atual

```text
89 passed
```

Os testes também são executados automaticamente através do **GitHub Actions** a cada alteração na branch `main` e em pull requests.

---

# ⚙️ Tecnologias

| Tecnologia        | Utilização                    |
| ----------------- | ----------------------------- |
| Python            | Linguagem principal           |
| Selenium          | Automação do WhatsApp Web     |
| SQLite            | Persistência local            |
| Pytest            | Testes automatizados          |
| WebDriver Manager | Gerenciamento do ChromeDriver |
| OpenAI API        | Integração com IA             |
| Git               | Controle de versão            |
| GitHub Actions    | Integração contínua           |

---

# ⚙️ Instalação

## 1. Clone o repositório

```bash
git clone https://github.com/jefersonsilva344/whatsapp-chatbot.git

cd whatsapp-chatbot
```

## 2. Crie o ambiente virtual

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

# 🔐 Configuração

Crie um arquivo `.env` local com as variáveis necessárias.

Exemplo:

```env
OPENAI_API_KEY=sua_chave_aqui
```

Nunca publique:

* API keys
* Tokens
* Credenciais
* Sessões do WhatsApp
* Arquivos `.env`

no GitHub.

---

# ▶️ Executando a aplicação

Com o ambiente virtual ativado:

```bash
python src/main.py
```

O chatbot iniciará a automação do WhatsApp Web utilizando Selenium.

Na primeira execução, será necessário realizar a autenticação no WhatsApp Web.

A sessão do navegador pode ser persistida localmente para evitar autenticação repetida, dependendo da configuração utilizada pela aplicação.

---

# ⚠️ Dados locais

Os seguintes arquivos e diretórios são utilizados localmente e não devem ser versionados:

```text
venv/
.env
data/*.db
data/*.sqlite
data/chrome_profile/
```

O diretório `chrome_profile` pode armazenar informações da sessão do navegador e, consequentemente, dados de autenticação do WhatsApp.

Por segurança, esse diretório deve permanecer fora do GitHub.

---

# 🔄 Integração Contínua

O projeto utiliza **GitHub Actions** para executar automaticamente a suíte de testes.

Fluxo:

```text
Push / Pull Request
        │
        ▼
GitHub Actions
        │
        ▼
Setup Python
        │
        ▼
Instalação das dependências
        │
        ▼
Pytest
        │
        ▼
89 testes
        │
        ▼
Build validado
```

Isso ajuda a detectar regressões antes que novas alterações sejam incorporadas ao projeto.

---

# 🎯 Objetivos técnicos

O projeto foi desenvolvido com foco em:

* Arquitetura modular
* Separação de responsabilidades
* Baixo acoplamento
* Injeção de dependências
* Persistência de dados
* Gerenciamento de estado
* Gerenciamento de sessões
* Automação web
* Integração com IA
* Testes unitários
* Testes de integração
* Integração contínua
* Manutenibilidade
* Evolução incremental

---

# 📈 Possíveis evoluções

Algumas melhorias planejadas para futuras versões:

* Dashboard para monitoramento
* Sistema de métricas
* Logs estruturados
* Dockerização
* Banco de dados externo
* API REST
* Sistema de autenticação
* Filas para processamento de mensagens
* Melhorias na camada de IA
* Deploy em ambiente cloud
* Observabilidade
* Monitoramento de erros
* Expansão dos fluxos de atendimento

---

# ⚖️ Aviso

Este projeto foi desenvolvido para fins **educacionais, experimentais e de portfólio**.

A utilização de automações no WhatsApp deve respeitar os termos de uso da plataforma e as regras aplicáveis ao envio de mensagens automatizadas.

---

# 👨‍💻 Autor

**Jeferson Silva**

Projeto desenvolvido como parte do portfólio de desenvolvimento **Python, automação, arquitetura de software, testes automatizados e integração com IA**.
