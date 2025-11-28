# 📦 Versões do Executável

O sistema possui **2 versões** do executável, cada uma para um propósito diferente:

---

## 🚀 Versão 1: PRODUÇÃO (Sem Console)

**Arquivo**: `EnviaEmailSRPP.exe`

### Características:
- ✅ **Sem janela de console** (roda em background)
- ✅ **Invisível para o usuário** (apenas no Gerenciador de Tarefas)
- ✅ **Não pode ser fechado acidentalmente**
- ✅ **Inicia automaticamente com Windows**
- ✅ **Logs gravados em arquivo**

### Quando Usar:
- ✅ Instalação em máquinas de produção
- ✅ Execução automática em background
- ✅ Ambiente onde usuários não devem interagir
- ✅ Inicialização automática do Windows

### Como Parar:
1. **Gerenciador de Tarefas** (Ctrl+Shift+Esc)
   - Procure: `EnviaEmailSRPP.exe`
   - Clique com direito → Finalizar tarefa

2. **Prompt como Admin**:
   ```bash
   taskkill /F /IM EnviaEmailSRPP.exe
   ```

### Como Verificar se Está Rodando:
- Abra o Gerenciador de Tarefas (Ctrl+Shift+Esc)
- Vá na aba "Processos"
- Procure por "EnviaEmailSRPP.exe"

### Como Ver os Logs:
- **Arquivo**: `logs\envio_emails.log`
- **Excel**: `C:\Users\Public\Documents\SRPP\scripts\log_emails_YYYY-MM-DD.xlsx`

---

## 🔧 Versão 2: DEBUG (Com Console)

**Arquivo**: `EnviaEmailSRPP_Debug.exe`

### Características:
- ✅ **Com janela de console** (mostra logs em tempo real)
- ✅ **Visível para o usuário**
- ✅ **Logs aparecem na tela** conforme acontecem
- ✅ **Fácil de parar** (Ctrl+C ou fechar janela)
- ✅ **Ideal para diagnóstico**

### Quando Usar:
- ✅ Testes e desenvolvimento
- ✅ Diagnóstico de problemas
- ✅ Verificar se emails estão sendo enviados
- ✅ Acompanhar processamento em tempo real
- ✅ Primeira configuração do sistema

### Como Parar:
1. **Ctrl+C** na janela de console
2. **Fechar** a janela (botão X)
3. **Gerenciador de Tarefas** (se necessário)

### Como Ver os Logs:
- **Na tela** (console mostra em tempo real)
- **Arquivo**: `logs\envio_emails.log` (também grava)
- **Excel**: `C:\Users\Public\Documents\SRPP\scripts\log_emails_YYYY-MM-DD.xlsx`

---

## 🎯 Guia Rápido de Escolha

| Situação | Versão Recomendada |
|----------|-------------------|
| Instalação final em máquinas | **PRODUÇÃO** (sem console) |
| Testar configurações | **DEBUG** (com console) |
| Diagnosticar problemas | **DEBUG** (com console) |
| Ver logs em tempo real | **DEBUG** (com console) |
| Execução automática 24/7 | **PRODUÇÃO** (sem console) |
| Primeira vez configurando | **DEBUG** (com console) |
| Servidor ou máquina remota | **PRODUÇÃO** (sem console) |

---

## 🔨 Como Gerar as Duas Versões

### Método Automático (Recomendado):
```bash
build_duas_versoes.bat
```

Este script gera **automaticamente** as 2 versões!

### Método Manual:

**Versão Produção (sem console):**
```bash
pyinstaller sender_producao.spec --clean --noconfirm
```

**Versão Debug (com console):**
```bash
pyinstaller sender_debug.spec --clean --noconfirm
```

---

## 📊 Comparação Técnica

| Característica | PRODUÇÃO | DEBUG |
|---------------|----------|-------|
| Janela de Console | ❌ Não | ✅ Sim |
| Logs em Tempo Real | ❌ Não | ✅ Sim |
| Logs em Arquivo | ✅ Sim | ✅ Sim |
| Roda em Background | ✅ Sim | ⚠️ Não |
| Fácil de Parar | ⚠️ Gerenciador | ✅ Ctrl+C |
| Uso de Memória | ~30 MB | ~30 MB |
| Tamanho do Arquivo | ~15 MB | ~15 MB |
| Velocidade | Idêntica | Idêntica |

---

## 💡 Dicas Importantes

### Para Produção:
1. **Sempre teste com a versão DEBUG primeiro**
2. Configure tudo e verifique se funciona
3. Depois distribua a versão PRODUÇÃO
4. Mantenha logs ativados para diagnóstico

### Para Debug/Testes:
1. Use para configuração inicial
2. Verifique se emails estão sendo enviados
3. Teste mudanças no `config.ini`
4. Diagnostique problemas antes de ir para produção

### Inicialização Automática (Produção):
1. Copie `EnviaEmailSRPP.exe` para a pasta do sistema
2. Crie atalho em:
   - **Windows 10/11**: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`
   - **Por usuário**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

### Monitoramento:
- Configure alertas para monitorar o processo
- Verifique logs diariamente
- Use a versão DEBUG se suspeitar de problemas

---

## 🆘 Solução de Problemas

### Versão PRODUÇÃO não inicia:
1. Teste com a versão **DEBUG** primeiro
2. Verifique logs em `logs\envio_emails.log`
3. Verifique Gerenciador de Tarefas se está rodando

### Não sei se está funcionando:
1. Abra `logs\envio_emails.log`
2. Ou use versão **DEBUG** para ver em tempo real

### Preciso parar urgentemente:
1. Gerenciador de Tarefas → EnviaEmailSRPP.exe → Finalizar
2. Ou comando: `taskkill /F /IM EnviaEmailSRPP.exe`

---

**Versão**: 1.0.0
**Data**: 2025-11-28
**Dúvidas**: Consulte `INSTALACAO.md` ou `COMO_GERAR_EXE.md`
