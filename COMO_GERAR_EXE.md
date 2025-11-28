# 🔨 Como Gerar o Executável (.exe) e Instalador

## ⚡ Método Rápido (Recomendado)

### Passo 1: Execute o script automático

```bash
criar_instalador_completo.bat
```

Este script fará **TUDO** automaticamente:
- ✅ Instala dependências necessárias
- ✅ Compila o executável
- ✅ Cria o instalador profissional (se Inno Setup estiver instalado)

---

## 📦 Método Manual

### Etapa 1: Instalar PyInstaller

Abra o terminal (CMD ou PowerShell) e execute:

```bash
pip install pyinstaller
```

### Etapa 2: Compilar o Executável

**Opção A - Script Automático:**
```bash
build.bat
```

**Opção B - Comando Manual:**
```bash
pyinstaller sender.spec --clean --noconfirm
```

O executável será criado em: `dist\EnviaEmailSRPP.exe`

### Etapa 3: Criar Instalador Profissional (Opcional)

1. **Baixe e Instale o Inno Setup**
   - Download: https://jrsoftware.org/isdl.php
   - Instale a versão mais recente (6.x)
   - Use o caminho de instalação padrão

2. **Compile o Instalador**
   - Opção A: Execute `criar_instalador_completo.bat`
   - Opção B: Abra `installer.iss` no Inno Setup Compiler e clique em "Compile"

O instalador será criado em: `installer_output\EnviaEmailSRPP_Setup_v1.0.0.exe`

---

## 📋 O que cada arquivo faz?

| Arquivo | Descrição |
|---------|-----------|
| `sender.spec` | Configuração do PyInstaller (dependências, ícone, etc.) |
| `version_info.txt` | Informações de versão do executável |
| `build.bat` | Script que compila apenas o EXE |
| `installer.iss` | Script do Inno Setup para criar instalador |
| `criar_instalador_completo.bat` | Script master que faz tudo |

---

## 🎯 Resultado Final

Após executar com sucesso, você terá:

### 1. Executável Standalone
```
dist\EnviaEmailSRPP.exe          (~15 MB)
```
- Pode ser copiado diretamente para qualquer máquina
- Não precisa de instalador
- **AINDA PRECISA** criar o `config.ini` manualmente

### 2. Instalador Profissional (Recomendado)
```
installer_output\EnviaEmailSRPP_Setup_v1.0.0.exe    (~15 MB)
```
- Instala o sistema completo
- Cria atalhos automaticamente
- Cria `config.ini` a partir do template
- Permite desinstalação via Painel de Controle
- **Este é o arquivo para distribuir!**

---

## 🔍 Verificação

### Teste o Executável

1. **Teste Rápido**
   ```bash
   dist\EnviaEmailSRPP.exe --teste
   ```
   - Este modo não envia emails
   - Apenas verifica conexão com banco e detecção de PDFs

2. **Teste Completo**
   - Configure o `config.ini`
   - Execute normalmente: `dist\EnviaEmailSRPP.exe`
   - Verifique os logs em `logs\envio_emails.log`

### Teste o Instalador

1. Execute `EnviaEmailSRPP_Setup_v1.0.0.exe`
2. Siga o assistente de instalação
3. Configure as credenciais quando solicitado
4. Execute o sistema

---

## ⚠️ Problemas Comuns

### Erro: "pip não é reconhecido"
**Solução**: Python não está no PATH
```bash
python -m pip install pyinstaller
```

### Erro: "pyinstaller não é reconhecido"
**Solução**: PyInstaller não está no PATH
```bash
python -m PyInstaller sender.spec --clean --noconfirm
```

### Erro: "Failed to execute script"
**Solução**: Falta dependência
- Verifique se todas as bibliotecas estão instaladas:
```bash
pip install pyodbc watchdog openpyxl
```

### Windows Defender bloqueia o EXE
**Solução**: Normal para executáveis não assinados
1. Adicione exceção no Windows Defender
2. Ou assine digitalmente o executável (requer certificado)

### Inno Setup não encontrado
**Solução**: Instale no caminho padrão
- `C:\Program Files (x86)\Inno Setup 6\`
- Ou edite o caminho em `criar_instalador_completo.bat`

---

## 🚀 Distribuição

### Para Distribuir o Sistema:

**Opção 1 - Instalador (Recomendado)**
- Envie apenas: `EnviaEmailSRPP_Setup_v1.0.0.exe`
- Tamanho: ~15-20 MB
- Usuário executa e segue o assistente

**Opção 2 - Executável Standalone**
- Crie um ZIP com:
  - `EnviaEmailSRPP.exe`
  - `config.ini.example` (renomear para `config.ini`)
  - `README.md`
  - `INSTALACAO.md`
- Usuário descompacta e configura manualmente

---

## 📝 Checklist de Build

Antes de distribuir, verifique:

- [ ] Código sem erros
- [ ] `config.ini.example` atualizado
- [ ] Versão atualizada em `version_info.txt`
- [ ] Versão atualizada em `installer.iss`
- [ ] Build executado com sucesso
- [ ] EXE testado em modo `--teste`
- [ ] EXE testado com envio real de email
- [ ] Instalador criado (se usar Inno Setup)
- [ ] Instalador testado em máquina limpa
- [ ] Documentação atualizada

---

## 🔐 Assinatura Digital (Opcional)

Para evitar avisos do Windows Defender:

1. **Adquira um Certificado de Assinatura de Código**
   - Empresas: Sectigo, DigiCert, etc.
   - Custo: ~R$ 500-1000/ano

2. **Assine o Executável**
   ```bash
   signtool sign /f certificado.pfx /p senha /t http://timestamp.digicert.com EnviaEmailSRPP.exe
   ```

3. **Assine o Instalador**
   - Mesma coisa para o arquivo `.exe` do instalador

**Nota**: Não é obrigatório, mas reduz avisos de segurança.

---

## 🎓 Recursos Adicionais

- **PyInstaller**: https://pyinstaller.org/
- **Inno Setup**: https://jrsoftware.org/isinfo.php
- **Assinatura de Código**: https://docs.microsoft.com/en-us/windows/win32/seccrypto/signtool

---

**Versão**: 1.0.0
**Data**: 2025-11-28
**Dúvidas?**: Consulte `INSTALACAO.md` ou os logs em `logs/`
