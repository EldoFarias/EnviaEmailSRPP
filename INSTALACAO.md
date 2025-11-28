# Guia de Instalação - Sistema de Envio Email SRPP

## 📋 Pré-requisitos

Antes de instalar o sistema, certifique-se de ter:

### 1. SQL Server ODBC Driver 17
- **Download**: https://go.microsoft.com/fwlink/?linkid=2249004
- Instale o driver apropriado para sua arquitetura (x64 ou x86)

### 2. Acesso ao Banco de Dados
- Servidor SQL Server com banco SRPP
- Credenciais de acesso (usuário e senha)

### 3. Conta de Email
- Gmail com senha de app OU
- Outlook/Hotmail com senha normal

---

## 🚀 Método 1: Instalador Profissional (RECOMENDADO)

### Passo 1: Baixar o Instalador
- Baixe `EnviaEmailSRPP_Setup_v1.0.0.exe`

### Passo 2: Executar o Instalador
1. **Execute como Administrador**
   - Clique com botão direito no instalador
   - Selecione "Executar como administrador"

2. **Siga o Assistente**
   - Aceite o diretório padrão: `C:\Program Files\SINT\EnviaEmailSRPP`
   - Escolha se deseja:
     - ✅ Criar atalho na área de trabalho
     - ✅ Iniciar automaticamente com Windows

3. **Configuração Inicial**
   - Ao final, o instalador abrirá o `config.ini`
   - Configure suas credenciais (veja seção abaixo)

### Passo 3: Configurar Credenciais

Edite o arquivo `config.ini` com suas informações:

```ini
[SQL_SERVER]
servidor = SEU_SERVIDOR
banco_de_dados = SRPP
usuario = SEU_USUARIO
senha = SUA_SENHA
driver = ODBC Driver 17 for SQL Server

[PDFS]
caminho = C:\Users\Public\Documents\SRPP\PDFs

[EMAIL]
smtp_servidor = smtp.gmail.com
smtp_porta = 587
usuario = seu_email@gmail.com
senha_app = sua_senha_app_sem_espacos
remetente_nome = VENDAS SINT
```

#### 📧 Configuração de Email Gmail

1. **Ativar Verificação em 2 Etapas**
   - Acesse: https://myaccount.google.com/security
   - Ative "Verificação em duas etapas"

2. **Gerar Senha de App**
   - Acesse: https://myaccount.google.com/apppasswords
   - Selecione "Outro (nome personalizado)"
   - Digite: "Sistema SRPP"
   - Clique em "Gerar"
   - **IMPORTANTE**: Copie a senha **SEM ESPAÇOS**
   - Exemplo: Se mostrar `abcd efgh ijkl mnop`, use `abcdefghijklmnop`

#### 📧 Configuração de Email Outlook

```ini
smtp_servidor = smtp-mail.outlook.com
smtp_porta = 587
usuario = seu_email@outlook.com
senha_app = sua_senha_normal
```

### Passo 4: Executar o Sistema
- Execute pelo atalho criado OU
- Execute `EnviaEmailSRPP.exe` manualmente

---

## 🔧 Método 2: Build Manual (Para Desenvolvedores)

### Passo 1: Instalar Dependências

```bash
pip install pyinstaller pyodbc watchdog openpyxl
```

### Passo 2: Compilar Executável

```bash
build.bat
```

O executável será criado em: `dist\EnviaEmailSRPP.exe`

### Passo 3: Criar Instalador (Opcional)

1. **Instale o Inno Setup**
   - Download: https://jrsoftware.org/isdl.php
   - Instale a versão mais recente

2. **Compile o Instalador**
   - Abra `installer.iss` no Inno Setup Compiler
   - Clique em "Build" → "Compile"
   - O instalador será criado em: `installer_output\EnviaEmailSRPP_Setup_v1.0.0.exe`

---

## 🛡️ Segurança e Firewall

### Windows Defender / Antivírus

Se o Windows Defender bloquear o executável:

1. **Adicionar Exceção**
   - Abra "Segurança do Windows"
   - Vá em "Proteção contra vírus e ameaças"
   - Clique em "Gerenciar configurações"
   - Role até "Exclusões" e clique em "Adicionar ou remover exclusões"
   - Adicione a pasta: `C:\Program Files\SINT\EnviaEmailSRPP`

2. **Executar como Administrador**
   - Isso pode resolver problemas de permissão

### Firewall do Windows

O sistema precisa de acesso à internet para:
- Conectar ao servidor de email (porta 587)
- Conectar ao SQL Server (porta padrão 1433)

Se bloqueado:
1. Abra "Firewall do Windows"
2. Clique em "Permitir um aplicativo pelo Firewall"
3. Clique em "Alterar configurações"
4. Clique em "Permitir outro aplicativo"
5. Adicione: `C:\Program Files\SINT\EnviaEmailSRPP\EnviaEmailSRPP.exe`
6. Marque "Redes privadas" e "Redes públicas"

---

## 📂 Estrutura de Arquivos

Após a instalação:

```
C:\Program Files\SINT\EnviaEmailSRPP\
├── EnviaEmailSRPP.exe       # Executável principal
├── config.ini               # Configurações (EDITE ESTE!)
├── config.ini.example       # Modelo de configuração
├── README.md                # Documentação
└── logs\                    # Pasta de logs
    └── envio_emails.log     # Log de operações
```

---

## 🔍 Verificação e Testes

### Teste Modo Debug (Sem Enviar Emails)

```bash
EnviaEmailSRPP.exe --teste
```

Este modo:
- ✅ Conecta ao banco de dados
- ✅ Busca pedidos para processar
- ✅ Detecta versões de PDF
- ❌ **NÃO** envia emails

### Logs

Verifique os logs em:
- **Arquivo**: `logs\envio_emails.log`
- **Excel**: `C:\Users\Public\Documents\SRPP\scripts\log_emails_YYYY-MM-DD.xlsx`

---

## ❓ Solução de Problemas

### Erro: "ODBC Driver not found"
**Solução**: Instale o ODBC Driver 17 for SQL Server
- Download: https://go.microsoft.com/fwlink/?linkid=2249004

### Erro: "Username and Password not accepted"
**Solução**: Verifique senha de app do Gmail
- Remova todos os espaços da senha
- Gere nova senha de app se necessário

### Erro: "Arquivo config.ini não encontrado"
**Solução**: Copie `config.ini.example` para `config.ini`

### PDF não é detectado
**Solução**: Verifique:
- Caminho da pasta de PDFs no `config.ini`
- Permissões de leitura na pasta
- Nome do arquivo PDF segue padrão: `PEDIDO 0000001.pdf`

---

## 🔄 Atualização

Para atualizar:
1. Desinstale a versão antiga
2. Instale a nova versão
3. **IMPORTANTE**: Suas configurações em `config.ini` são preservadas

---

## 🗑️ Desinstalação

### Via Painel de Controle
1. Abra "Adicionar ou Remover Programas"
2. Procure por "Sistema de Envio Email SRPP"
3. Clique em "Desinstalar"

### Manual
Delete a pasta: `C:\Program Files\SINT\EnviaEmailSRPP`

---

## 📞 Suporte

Em caso de problemas:
1. Verifique os logs em `logs\envio_emails.log`
2. Execute em modo teste: `EnviaEmailSRPP.exe --teste`
3. Consulte este guia de instalação
4. Contate o suporte técnico da SINT

---

## ✅ Checklist de Instalação

- [ ] ODBC Driver 17 instalado
- [ ] Executável baixado ou compilado
- [ ] Sistema instalado
- [ ] config.ini configurado com credenciais corretas
- [ ] Senha de app do Gmail gerada (sem espaços)
- [ ] Pasta de PDFs configurada
- [ ] Teste executado com sucesso
- [ ] Sistema rodando sem erros

---

**Versão**: 1.0.0
**Data**: 2025-11-28
**Empresa**: SINT
