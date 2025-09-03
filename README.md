# 🤖 J.A.R.V.I.S - Assistente Virtual Inteligente com Integração Arduino

## 📋 Projeto de TCC - ETEC Bento Quirino

### 🎯 Resumo Executivo

O **J.A.R.V.I.S** (Just A Rather Very Intelligent System) é um assistente virtual inteligente desenvolvido em Python que integra tecnologias de reconhecimento de voz, inteligência artificial e controle de hardware através de Arduino. O projeto demonstra a convergência entre software e hardware, criando uma interface homem-máquina mais intuitiva e interativa.

---

## 🚀 Funcionalidades Principais

### 🎤 Reconhecimento de Voz
- **Hotword Detection**: Ativação por palavra-chave "Jarvis"
- **Comandos de Voz**: Reconhecimento de comandos em português brasileiro
- **Processamento Natural**: Integração com OpenAI GPT para conversas inteligentes

### 🎵 Controle de Mídia
- **Spotify Integration**: Reprodução de músicas e playlists
- **YouTube Integration**: Busca e reprodução de vídeos
- **Sistema de Favoritos**: Gerenciamento de músicas favoritas
- **Playlists Especiais**: Foco, relaxamento e animação

### 💻 Controle de Sistema
- **Atalhos de Teclado**: Copiar, colar, minimizar, print screen
- **Controle de Aplicativos**: Abertura de programas do sistema
- **Gerenciamento de Janelas**: Fechamento por palavra-chave
- **Controle de Mouse**: Desenho de formas geométricas

### 🔍 Pesquisa e Informação
- **Google Search**: Pesquisas na web
- **Wikipedia**: Resumos e informações
- **Notícias**: G1 e Omelete
- **Timer e Pomodoro**: Gerenciamento de tempo

### 🎨 Interface Visual
- **GUI Animada**: Interface gráfica com animações
- **Modo Apresentação**: Otimizado para demonstrações
- **Feedback Visual**: Mudança de cores conforme estado

---

## 🔧 Integração Arduino

### 💡 Controle de LED
- **LED Indicador**: Acende quando JARVIS está ativo
- **Feedback Visual**: Sincronização com ações de voz
- **Comunicação Serial**: Protocolo simples e eficiente

### 🔌 Hardware Utilizado
- **Arduino UNO**: Microcontrolador principal
- **LED Built-in**: Pino 13 (ou LED externo com resistor 220Ω)
- **Conexão USB**: Comunicação serial com computador

### 📡 Protocolo de Comunicação
```
Comandos Arduino:
- '1' = Liga LED
- '0' = Desliga LED
- Baud Rate: 9600
- Detecção automática de porta COM
```

---

## 🛠️ Tecnologias Utilizadas

### 🐍 Backend (Python)
- **Speech Recognition**: Reconhecimento de voz
- **pyttsx3**: Síntese de voz
- **OpenAI GPT**: Inteligência artificial conversacional
- **tkinter**: Interface gráfica
- **pyserial**: Comunicação com Arduino
- **spotipy**: API do Spotify
- **yt-dlp**: Download de vídeos do YouTube

### 🔌 Hardware
- **Arduino UNO**: Microcontrolador
- **LED**: Indicador visual
- **Cabo USB**: Comunicação serial

### ☁️ APIs Externas
- **OpenAI GPT-3.5**: Processamento de linguagem natural
- **Spotify Web API**: Controle de música
- **Google Speech-to-Text**: Reconhecimento de voz
- **Wikipedia API**: Busca de informações

---

## 📦 Instalação e Configuração

### �� Pré-requisitos
```bash
# Python 3.8+
# Arduino IDE
# Microfone funcional
# Alto-falantes
```

### 📋 Dependências Python
```bash
pip install speech_recognition
pip install pyttsx3
pip install openai
pip install pyserial
pip install spotipy
pip install yt-dlp
pip install wikipedia
pip install requests
pip install beautifulsoup4
pip install pyautogui
pip install opencv-python
pip install numpy
pip install psutil
pip install pygetwindow
pip install langdetect
```

### 🔑 Configuração de APIs
```bash
# OpenAI API Key
export OPENAI_API_KEY="sua_chave_aqui"

# Spotify (opcional)
export SPOTIPY_CLIENT_ID="seu_client_id"
export SPOTIPY_CLIENT_SECRET="seu_client_secret"
export SPOTIPY_REDIRECT_URI="http://localhost:8080/callback"
```

### 🔌 Configuração Arduino
1. **Conecte o Arduino** via USB
2. **Carregue o código** `JARVIS_Arduino_LED.ino`
3. **Verifique a porta COM** (detecção automática)
4. **Teste o LED** (pisca 3 vezes na inicialização)

---

## 🚀 Como Usar

### 🎤 Comandos de Voz Principais
```
"Jarvis" - Ativa o assistente
"ligar led" / "acender led" - Controle manual do LED
"tocar [música] no spotify" - Reproduzir música
"pesquisar [termo] no google" - Busca na web
"timer 25 minutos" - Iniciar pomodoro
"modo apresentação" - Ativar modo demonstração
```

### 🎵 Controle de Música
```
"tocar favoritos" - Reproduzir músicas salvas
"playlist de foco" - Música para concentração
"playlist relaxar" - Música para relaxamento
"salvar [música] como favorito" - Adicionar aos favoritos
```

### 💻 Controle de Sistema
```
"copiar" / "colar" - Atalhos de teclado
"abrir calculadora" - Aplicativos do sistema
"fechar janela [nome]" - Gerenciar janelas
"círculo" - Desenhar com mouse
```

---

## 📊 Estrutura do Projeto

```
JARVIS/
├── V0.7.py                    # Versão original
├── JARVIS_v0.8_Arduino.py     # Versão com Arduino
├── JARVIS_Arduino_LED.ino     # Código Arduino
├── README.md                  # Documentação
├── jarvis_memory.json         # Memória do sistema
├── ICONS/                     # Ícones da interface
└── [GUIA DE INSTALAÇÃO].docx  # Manual detalhado
```

---

## 🧠 Arquitetura do Sistema

### 🔄 Fluxo de Funcionamento
1. **Hotword Detection** → Detecta "Jarvis"
2. **Voice Recognition** → Processa comando de voz
3. **Command Routing** → Roteia para função específica
4. **Action Execution** → Executa ação solicitada
5. **Arduino Control** → Controla LED conforme ação
6. **Voice Response** → Responde ao usuário

### 💾 Sistema de Memória
- **Histórico de Conversas**: Últimas 100 interações
- **Preferências do Usuário**: Idioma, modo apresentação
- **Favoritos Musicais**: Lista de músicas salvas
- **Configurações Arduino**: Porta e configurações

---

## 🎓 Objetivos Educacionais

### 📚 Competências Desenvolvidas
- **Programação Python**: Lógica e estrutura de dados
- **Integração Hardware-Software**: Comunicação serial
- **APIs e Web Services**: Consumo de APIs externas
- **Interface Homem-Máquina**: Design de UX
- **Inteligência Artificial**: Processamento de linguagem natural
- **Sistemas Embarcados**: Programação Arduino

### 🔬 Metodologia
- **Pesquisa Aplicada**: Desenvolvimento de solução real
- **Integração de Tecnologias**: Convergência de diferentes áreas
- **Prototipagem**: Desenvolvimento iterativo
- **Testes e Validação**: Verificação de funcionalidades

---

## 📈 Resultados Esperados

### 🎯 Objetivos Alcançados
- ✅ Assistente virtual funcional
- ✅ Integração Arduino bem-sucedida
- ✅ Interface gráfica responsiva
- ✅ Controle de mídia integrado
- ✅ Sistema de comandos de voz
- ✅ Documentação completa

### 📊 Métricas de Sucesso
- **Taxa de Reconhecimento**: >90% de comandos reconhecidos
- **Tempo de Resposta**: <2 segundos para comandos simples
- **Estabilidade**: Sistema estável por longos períodos
- **Usabilidade**: Interface intuitiva e acessível

---

## 🔮 Futuras Melhorias

### 🚀 Funcionalidades Planejadas
- **Reconhecimento Facial**: Identificação do usuário
- **Controle de IoT**: Integração com dispositivos smart home
- **Machine Learning**: Aprendizado de preferências
- **Interface Web**: Dashboard remoto
- **Multi-idioma**: Suporte a outros idiomas
- **Cloud Integration**: Sincronização de dados

### 🎨 Melhorias de Interface
- **Interface Touch**: Controle por toque
- **Reconhecimento Gestual**: Controle por gestos
- **Realidade Aumentada**: Overlay de informações
- **Personalização**: Temas e customizações

---

## 👥 Autores e Orientação

### 👨‍🎓 Desenvolvedor
- **Nome**: [Seu Nome]
- **Curso**: Desenvolvimento de Sistemas
- **Instituição**: ETEC Bento Quirino
- **Período**: último

### 👨‍🏫 Orientador
- **Nome**: [Nome do Orientador]
- **Área**: [Área de Especialização]

### 📅 Cronograma
- **Início**: [Data de Início]
- **Desenvolvimento**: [Período de Desenvolvimento]
- **Testes**: [Período de Testes]
- **Apresentação**: [Data de Apresentação]

---

## 📄 Licença e Uso

### 📋 Termos de Uso
- **Uso Educacional**: Projeto desenvolvido para fins educacionais
- **Código Aberto**: Disponível para estudo e modificação
- **Atribuição**: Mantenha os créditos aos autores
- **Responsabilidade**: Uso por conta e risco do usuário

### 🔒 Privacidade
- **Dados Locais**: Informações armazenadas localmente
- **APIs Externas**: Respeito às políticas de privacidade
- **Não Rastreamento**: Sistema não coleta dados pessoais

---

## 📞 Suporte e Contato

### 💬 Comunicação
- **Email**: [seu.email@exemplo.com]
- **GitHub**: [link-do-github]
- **LinkedIn**: [link-do-linkedin]

### 🐛 Reportar Problemas
- **Issues**: Use o sistema de issues do GitHub
- **Documentação**: Consulte este README
- **FAQ**: Seção de perguntas frequentes

---

## 🙏 Agradecimentos

### 🏫 Instituição
- **ETEC Bento Quirino**: Suporte institucional
- **Professores**: Orientação e conhecimento
- **Colegas**: Colaboração e feedback

### 🛠️ Recursos Utilizados
- **OpenAI**: API de inteligência artificial
- **Arduino**: Plataforma de desenvolvimento
- **Comunidade Python**: Bibliotecas e suporte
- **Stack Overflow**: Resolução de problemas

---

## 📚 Referências Bibliográficas

### 📖 Bibliografia
1. **Python Documentation**: [link]
2. **Arduino Reference**: [link]
3. **Speech Recognition**: [link]
4. **OpenAI API**: [link]
5. **Spotify Web API**: [link]

### 🔗 Links Úteis
- **Repositório**: [link-do-repositorio]
- **Documentação**: [link-da-documentacao]
- **Demonstração**: [link-da-demo]

---

*Desenvolvido com ❤️ para o TCC da ETEC Bento Quirino*

**Versão**: 0.8 - Arduino Integration  
**Última Atualização**: Setembro 2025  
**Status**: ✅ Concluído