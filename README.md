# 🤖 WhatsApp Chatbot — Automação Inteligente de Atendimento

<p align="center">
  <strong>Chatbot automatizado para atendimento via WhatsApp Web, desenvolvido em Python com arquitetura modular, persistência em SQLite, máquina de estados, testes automatizados e integração com Inteligência Artificial.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Selenium-Automation-green?logo=selenium" alt="Selenium">
  <img src="https://img.shields.io/badge/SQLite-Database-lightgrey?logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/Pytest-89%20tests-success?logo=pytest" alt="Pytest">
  <img src="https://img.shields.io/badge/GitHub%20Actions-CI-blue?logo=githubactions" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/OpenAI-API-black?logo=openai" alt="OpenAI">
</p>

---

## 📌 Sobre o projeto

O **WhatsApp Chatbot** é uma aplicação de automação de atendimento desenvolvida em Python para interagir com o **WhatsApp Web** utilizando Selenium.

O projeto foi construído com uma abordagem de engenharia de software, buscando superar o modelo tradicional de automação baseada em scripts e concentrando-se em:

* Arquitetura modular
* Separação de responsabilidades
* Baixo acoplamento
* Injeção de dependências
* Gerenciamento de sessões
* Máquina de estados
* Processamento e deduplicação de mensagens
* Persistência de dados
* Integração com Inteligência Artificial
* Testes unitários e de integração
* Integração contínua com GitHub Actions

A aplicação foi estruturada para que os principais componentes possam ser desenvolvidos, testados e evoluídos de forma independente.

### 🎯 Objetivo

O objetivo principal é demonstrar a construção de uma aplicação real de automação de atendimento, combinando:

**Automação Web + Backend Python + Banco de Dados + Arquitetura de Software + Testes + IA + CI/CD**

---

# 🚀 Principais funcionalidades

## 💬 Automação do WhatsApp

* Automação do WhatsApp Web através do Selenium
* Leitura de mensagens recebidas
* Envio automático de respostas
* Abertura e gerenciamento de conversas
* Detecção de conversas não lidas
* Identificação do perfil utilizado pelo bot
* Monitoramento contínuo de novas mensagens

## 🧠 Processamento de mensagens

* Normalização de mensagens
* Processamento centralizado
* Controle de mensagens duplicadas
* Persistência do histórico
* Encaminhamento da mensagem para o fluxo adequado
* Geração e envio de respostas
* Registro das respostas enviadas

## 🔄 Gerenciamento de conversas

Cada conversa possui seu próprio contexto e ciclo de atendimento.

A aplicação utiliza:

* Gerenciamento de conversações
* Gerenciamento de sessões
* Máquina de estados
* Fluxos de atendimento
* Persistência do histórico
* Controle do estado atual da interação

Isso permite que o chatbot mantenha o contexto da conversa mesmo quando várias mensagens são processadas.

## 🤖 Inteligência Artificial

O projeto possui uma camada dedicada à integração com IA.

A arquitetura separa:

* Serviço de IA
* Memória/contexto
* Prompts
* Regras determinísticas
* Intenções
* Normalização
* Respostas

Essa abordagem permite utilizar regras programadas quando o comportamento precisa ser determinístico e IA quando existe necessidade de processamento mais flexível.

## 🗄️ Persistência

O projeto utiliza **SQLite** para armazenamento local.

São armazenados dados relacionados a:

* Mensagens
* Conversas
* Histórico de atendimento
* Sessões
* Estado das interações

O acesso ao banco é abstraído através de **Repository Pattern**, evitando que a lógica de negócio fique diretamente acoplada ao SQL.

## 🧪 Qualidade e testes

A aplicação possui uma suíte automatizada utilizando **Pytest**.

Atualmente:

**89 testes automatizados passando. ✅**

A cobertura de testes contempla componentes como:

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

Execução:

```bash
python -m pytest -v
```

---

# 🏗️ Arquitetura

O processamento principal da aplicação segue uma arquitetura modular:

```text
                         WhatsApp Web
                              │
                              ▼
                     ┌────────────────┐
                     │  WhatsAppBot   │
                     └───────┬────────┘
                             │
                             ▼
                     ┌────────────────┐
                     │    Monitor     │
                     └───────┬────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   MessageProcessor   │
                  └──────────┬───────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
       ┌────────────────────┐  ┌────────────────────┐
       │ ConversationManager│  │ MessageRepository  │
       └──────────┬─────────┘  └──────────┬─────────┘
                  │                       │
                  ▼                       ▼
       ┌────────────────────┐          SQLite
       │   SessionManager   │
       └──────────┬─────────┘
                  │
                  ▼
       ┌────────────────────┐
       │    StateManager    │
       └──────────┬─────────┘
                  │
                  ▼
       ┌────────────────────┐
       │    FlowManager     │
       └──────────┬─────────┘
                  │
            ┌─────┴─────┐
            ▼           ▼
      ┌──────────┐ ┌────────────────┐
      │ Responder│ │  OpenAIService │
      └────┬─────┘ └───────┬────────┘
           │               │
           └───────┬───────┘
                   ▼
              ┌──────────┐
              │ Resposta │
              └────┬─────┘
                   │
                   ▼
             WhatsApp Web
```

### 🔎 Responsabilidade dos principais componentes

| Componente               | Responsabilidade                            |
| ------------------------ | ------------------------------------------- |
| `WhatsAppBot`            | Inicialização e controle da automação       |
| `Monitor`                | Monitoramento das conversas e mensagens     |
| `MessageProcessor`       | Orquestração do processamento das mensagens |
| `ConversationManager`    | Gerenciamento das conversas                 |
| `SessionManager`         | Controle das sessões                        |
| `StateManager`           | Controle do estado atual                    |
| `FlowManager`            | Execução dos fluxos de atendimento          |
| `Responder`              | Aplicação de regras e geração de respostas  |
| `OpenAIService`          | Integração com IA                           |
| `MessageRepository`      | Persistência de mensagens                   |
| `ConversationRepository` | Persistência de conversas                   |
| `SQLite`                 | Armazenamento local                         |

Essa divisão reduz o acoplamento entre automação, regras de negócio, persistência e serviços externos.

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

O chatbot utiliza uma **máquina de estados** para controlar o ciclo de cada conversa.

Exemplo:

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

Cada estado possui uma responsabilidade específica e determina quais informações devem ser coletadas e qual será a próxima etapa.

Isso evita que a aplicação dependa exclusivamente do conteúdo da última mensagem recebida.

### Exemplo de atendimento

```text
Cliente
   │
   │ "Olá"
   ▼
INICIO
   │
   │ "Olá! Qual seu nome?"
   ▼
AGUARDANDO_NOME
   │
   │ "Jeferson"
   ▼
AGUARDANDO_SERVICO
   │
   │ "Preciso de instalação elétrica"
   ▼
ORCAMENTO
   │
   ▼
CONFIRMACAO
   │
   ▼
FINALIZADO
```

---

# 🧠 Integração com Inteligência Artificial

A integração com IA foi isolada em uma camada específica:

```text
src/ia/
│
├── memoria.py
├── openai_service.py
└── prompt.py
```

Essa arquitetura evita que a implementação da IA fique espalhada pelo restante da aplicação.

Além disso, o projeto possui uma camada de respostas baseada em regras:

```text
src/responder/
│
├── intents.py
├── normalizador.py
├── regras.py
├── responder.py
└── respostas.py
```

### Estratégia híbrida

A aplicação pode combinar:

```text
Mensagem
    │
    ▼
Normalização
    │
    ▼
Identificação do contexto
    │
    ├───────────────┐
    ▼               ▼
Regras           IA
    │               │
    └───────┬───────┘
            ▼
         Resposta
```

Essa abordagem permite manter comportamentos críticos previsíveis através de regras determinísticas, enquanto utiliza IA para situações que exigem maior flexibilidade.

As credenciais de serviços externos são obtidas através de variáveis de ambiente.

---

# 🗄️ Persistência de dados

O projeto utiliza **SQLite** como banco de dados local.

A comunicação com o banco é organizada através de repositories:

```text
MessageProcessor
       │
       ▼
MessageRepository
       │
       ▼
     SQLite
```

Essa abstração permite separar:

**Regra de negócio → Repository → Banco de dados**

Em vez de:

**Regra de negócio → SQL diretamente**

### Dados armazenados

* Mensagens recebidas
* Mensagens enviadas
* Conversas
* Histórico
* Dados relacionados às sessões
* Informações necessárias para controle do atendimento

---

# 🔐 Segurança

Informações sensíveis não devem ser armazenadas no código-fonte.

O projeto utiliza variáveis de ambiente para configurações sensíveis, por exemplo:

```env
OPENAI_API_KEY=sua_chave_aqui
```

Arquivos de configuração e dados locais devem permanecer fora do controle de versão:

```text
.env
venv/
data/*.db
data/*.sqlite
data/chrome_profile/
```

### ⚠️ Importante

O diretório `chrome_profile` pode conter informações relacionadas à sessão do navegador e autenticação do WhatsApp.

Por isso, **nunca deve ser publicado no GitHub**.

Também não devem ser versionados:

* API Keys
* Tokens
* Senhas
* Cookies
* Credenciais
* Sessões do WhatsApp
* Dados pessoais de usuários

---

# 🧪 Testes automatizados

O projeto possui uma suíte de testes construída com **Pytest**.

### Resultado atual

```text
89 passed
```

### Execução local

```bash
python -m pytest -v
```

### Camadas testadas

```text
Tests
 │
 ├── Container
 ├── Conversation Manager
 ├── Conversation Repository
 ├── Flow Manager
 ├── Message Processor
 ├── Message Repository
 ├── Monitor
 ├── Session Manager
 ├── State Manager
 ├── OpenAI Service
 └── Integration
```

A utilização de testes automatizados reduz regressões e permite evoluir a arquitetura com maior segurança.

---

# 🔄 Integração Contínua

O projeto utiliza **GitHub Actions** para automatizar a execução dos testes.

Fluxo:

```text
       Git Push / Pull Request
                 │
                 ▼
        ┌─────────────────┐
        │ GitHub Actions  │
        └────────┬────────┘
                 │
                 ▼
       Configuração do Python
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
          ┌──────┴──────┐
          ▼             ▼
       Sucesso        Falha
          │             │
          ▼             ▼
      Validação      Correção
```

O objetivo é detectar regressões automaticamente antes que alterações sejam incorporadas ao projeto.

---

# ⚙️ Tecnologias utilizadas

| Tecnologia            | Aplicação                              |
| --------------------- | -------------------------------------- |
| **Python**            | Desenvolvimento da aplicação           |
| **Selenium**          | Automação do WhatsApp Web              |
| **SQLite**            | Persistência local                     |
| **Pytest**            | Testes automatizados                   |
| **WebDriver Manager** | Gerenciamento do ChromeDriver          |
| **OpenAI API**        | Integração com IA                      |
| **python-dotenv**     | Gerenciamento de variáveis de ambiente |
| **Git**               | Controle de versão                     |
| **GitHub Actions**    | Integração contínua                    |

---

# 📦 Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/jefersonsilva344/whatsapp-chatbot.git
cd whatsapp-chatbot
```

## 2. Criar ambiente virtual

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

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

# 🔧 Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_aqui
```

Nunca compartilhe ou versione esse arquivo.

O `.gitignore` deve impedir que credenciais e dados locais sejam enviados para o repositório.

---

# ▶️ Executando a aplicação

Com o ambiente virtual ativado:

```bash
python src/main.py
```

A aplicação iniciará a automação do WhatsApp Web através do Selenium.

Na primeira execução, poderá ser necessário autenticar o WhatsApp Web.

Dependendo da configuração utilizada pelo projeto, o perfil do navegador pode ser persistido localmente para evitar uma nova autenticação em cada execução.

---

# 🧪 Executando os testes

Para executar toda a suíte:

```bash
python -m pytest -v
```

Para executar um arquivo específico:

```bash
python -m pytest src/tests/test_message_processor.py -v
```

Para executar o teste de integração:

```bash
python -m pytest src/tests/test_integration.py -v
```

---

Exemplo:

```text
Cliente envia mensagem
        ↓
Monitor identifica conversa
        ↓
Mensagem é processada
        ↓
Mensagem é persistida
        ↓
Estado da conversa é consultado
        ↓
Fluxo é executado
        ↓
Resposta é gerada
        ↓
Resposta enviada pelo WhatsApp
        ↓
Histórico atualizado
```

### Sugestão para o portfólio

Adicionar:

* GIF do chatbot respondendo
* Screenshot do WhatsApp Web
* Screenshot dos testes passando
* Screenshot do GitHub Actions
* Diagrama da arquitetura

Isso permite que recrutadores e clientes entendam rapidamente o resultado do projeto.

---

# 🎯 Competências demonstradas

Este projeto demonstra experiência prática em:

### Backend

* Desenvolvimento Python
* Programação orientada a objetos
* Modularização
* Gerenciamento de dependências
* Persistência de dados
* Repository Pattern
* Injeção de dependências

### Automação

* Selenium WebDriver
* Automação de navegador
* Localização de elementos
* Leitura e envio de mensagens
* Monitoramento de interfaces web

### Arquitetura

* Separação de responsabilidades
* Baixo acoplamento
* Máquina de estados
* Gerenciamento de sessões
* Fluxos de negócio
* Componentização

### Qualidade

* Testes unitários
* Testes de integração
* Pytest
* Testabilidade
* Prevenção de regressões

### IA

* Integração com API de IA
* Engenharia de prompts
* Gerenciamento de contexto
* Arquitetura híbrida entre regras e IA

### DevOps

* Git
* GitHub
* GitHub Actions
* CI
* Automação de testes

---

# 💼 Aplicações práticas

A arquitetura desenvolvida pode ser adaptada para diferentes cenários de atendimento automatizado, como:

* Atendimento comercial
* Pré-vendas
* Captação de leads
* Agendamento de serviços
* Orçamentos
* Suporte inicial
* Triagem de clientes
* FAQ automatizado
* Atendimento interno

A máquina de estados permite adaptar os fluxos de acordo com o processo de negócio.

---

# 📈 Possíveis evoluções

O projeto foi desenvolvido de forma incremental e possui espaço para evolução arquitetural.

### Próximas possibilidades

* Dashboard de atendimento
* Métricas de conversão
* Logs estruturados
* Observabilidade
* Monitoramento de erros
* Dockerização
* API REST
* Banco de dados PostgreSQL
* Sistema de autenticação
* Filas para processamento assíncrono
* Cache
* Sistema de métricas
* Deploy em cloud
* Webhook/API oficial para integração com WhatsApp
* Expansão dos fluxos de atendimento
* Melhorias na camada de IA
* Sistema de avaliação das respostas
* Painel administrativo

---

# 🧩 Desafios técnicos abordados

Durante o desenvolvimento, o projeto trabalhou com problemas comuns em sistemas de automação e atendimento:

### Deduplicação de mensagens

Mensagens recebidas podem ser processadas mais de uma vez. O sistema utiliza persistência e controle para evitar processamento duplicado.

### Estado da conversa

O chatbot precisa saber em qual etapa cada cliente está.

Por isso, o estado é controlado através de uma máquina de estados.

### Separação entre automação e negócio

A lógica de atendimento não deve depender diretamente do Selenium.

Por isso, a automação, o processamento, os fluxos e a persistência foram separados em módulos.

### Testabilidade

A arquitetura foi estruturada para permitir testes dos componentes sem depender constantemente da interface do WhatsApp Web.

---

# ⚖️ Aviso

Este projeto foi desenvolvido para fins **educacionais, experimentais e de portfólio**.

A utilização de automações no WhatsApp deve respeitar os termos de uso da plataforma, políticas aplicáveis e regras relacionadas ao envio de mensagens automatizadas.

Para aplicações comerciais em produção, recomenda-se avaliar o uso das APIs oficiais e das soluções disponibilizadas pela Meta.

---

# 👨‍💻 Autor

## Jeferson Silva

Desenvolvedor com foco em **Python, automação, arquitetura de software, testes automatizados e integração com Inteligência Artificial**.

Este projeto faz parte do meu portfólio e demonstra a aplicação prática de conceitos de desenvolvimento de software em uma solução de automação de atendimento.

### 🔗 Projeto

**GitHub:**

https://github.com/jefersonsilva344/whatsapp-chatbot

---

## ⭐ Se este projeto foi útil

Se você gostou da arquitetura ou encontrou este projeto através do meu portfólio, considere deixar uma ⭐ no repositório.

Feedbacks, sugestões e contribuições são bem-vindos.
