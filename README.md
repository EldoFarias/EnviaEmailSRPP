# Sistema de Envio Automático de PDFs por Email - SRPP

Sistema automatizado que monitora uma pasta de PDFs e envia automaticamente por email quando novos pedidos são fechados no sistema SRPP.

## Funcionalidades

- Monitoramento em tempo real de pasta de PDFs
- Envio automático de emails com anexos
- Controle de versões de PDFs (detecta e reenvia versões atualizadas)
- Sistema de tentativas com cool-down progressivo
- Logs detalhados em arquivo e Excel
- Integração com SQL Server
- Suporte para cópias de email (CC)

## Requisitos

### Python 3.x

### Bibliotecas Python
```bash
pip install pyodbc
pip install watchdog
pip install openpyxl
```

### SQL Server ODBC Driver
- ODBC Driver 17 for SQL Server

## Configuração

1. Copie o arquivo `config.ini.example` para `config.ini`
2. Edite o `config.ini` com suas credenciais:

### Banco de Dados SQL Server
```ini
[SQL_SERVER]
servidor = 127.0.0.1
banco_de_dados = SRPP
usuario = sa
senha = SUA_SENHA
driver = ODBC Driver 17 for SQL Server
```

### Email (Gmail)
```ini
[EMAIL]
smtp_servidor = smtp.gmail.com
smtp_porta = 587
usuario = seu_email@gmail.com
senha_app = sua_senha_app_sem_espacos
remetente_nome = VENDAS SINT
```

**IMPORTANTE**: Para Gmail, você precisa:
1. Ativar verificação em 2 etapas: https://myaccount.google.com/security
2. Gerar senha de app: https://myaccount.google.com/apppasswords
3. Copiar a senha **SEM ESPAÇOS** para o config.ini

### Pasta de PDFs
```ini
[PDFS]
caminho = C:\Users\Public\Documents\SRPP\PDFs
```

## Como Executar

### Modo Normal (Produção)
```bash
python sender.py
```

### Modo Teste (Sem enviar emails)
```bash
python sender.py --teste
```

## Estrutura de Versões de PDF

O sistema detecta versões de PDF pelo nome do arquivo:
- `PEDIDO 0000001.pdf` - Versão 1
- `PEDIDO 0000001_2.pdf` - Versão 2
- `PEDIDO 0000001_3.pdf` - Versão 3

Quando uma nova versão é detectada, o sistema automaticamente reenvia o email.

## Logs

- **Arquivo de log**: `logs/envio_emails.log`
- **Excel detalhado**: `C:\Users\Public\Documents\SRPP\scripts\log_emails_YYYY-MM-DD.xlsx`

## Sistema de Tentativas

O sistema usa cool-down progressivo para tentativas:
- Tentativa 1: aguarda 2 minutos
- Tentativa 2: aguarda 5 minutos
- Tentativa 3: aguarda 10 minutos
- Tentativa 4: aguarda 20 minutos
- Tentativa 5+: aguarda 30 minutos

## Banco de Dados

O sistema requer a tabela `ControleEmailPedidos` no SQL Server com os seguintes campos:
- Id, NroPedido, CodCliente, DataPedidoFechado
- EmailsCopia, StatusProcessamento, EmailEnviado
- VersaoPdfEnviada, TentativasEnvio, UltimoErro
- DataEnvio

## Segurança

- **NUNCA** commite o arquivo `config.ini` (contém credenciais)
- Use o `.gitignore` para proteger informações sensíveis
- Mantenha as senhas de app do Gmail seguras

## Distribuição e Instalação

### 🚀 Gerar Executável e Instalador

Para criar o executável (.exe) e instalador profissional:

```bash
criar_instalador_completo.bat
```

Este script:
- Compila o código Python em executável standalone
- Cria instalador profissional do Windows
- Gera arquivo de ~15-20 MB pronto para distribuir

**Documentação completa**:
- `COMO_GERAR_EXE.md` - Guia completo de build
- `INSTALACAO.md` - Guia de instalação para usuários finais

### 📦 Arquivos Gerados

- **Executável**: `dist\EnviaEmailSRPP.exe`
- **Instalador**: `installer_output\EnviaEmailSRPP_Setup_v1.0.0.exe`

**Recomendação**: Distribua o instalador (mais profissional e fácil para o usuário)

## Suporte

Para problemas ou dúvidas:
1. Consulte `INSTALACAO.md` para guia detalhado
2. Consulte `COMO_GERAR_EXE.md` para problemas de build
3. Verifique os logs em `logs/envio_emails.log`
