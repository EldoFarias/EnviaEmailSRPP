# Configuração via Banco de Dados

## 📋 Visão Geral

A partir desta versão, o sistema **EnviaEmailSRPP** utiliza configurações armazenadas no **banco de dados SQL Server** em vez de depender exclusivamente do arquivo `config.ini`. Isso torna o sistema **mais robusto, flexível e seguro**.

---

## 🎯 Benefícios

### ✅ Antes (config.ini)
- ❌ Arquivo texto frágil e exposto
- ❌ Credenciais em texto plano no disco
- ❌ Assunto e corpo de email fixos no código
- ❌ Difícil de atualizar em produção
- ❌ Sem controle de versão das configurações

### ✅ Agora (Banco de Dados)
- ✅ Configurações centralizadas e seguras
- ✅ Credenciais protegidas no banco
- ✅ **Assunto e corpo de email parametrizáveis**
- ✅ Fácil atualização via SQL (sem reiniciar o sistema)
- ✅ Controle de versão e auditoria (campos `DataCriacao`, `DataAlteracao`)
- ✅ Múltiplas configurações (apenas uma ativa por vez)
- ✅ Fallback automático para `config.ini` se banco indisponível

---

## 🗄️ Tabela: ConfiguracaoSistema

### Estrutura da Tabela

```sql
CREATE TABLE dbo.ConfiguracaoSistema (
    Id INT IDENTITY(1,1) PRIMARY KEY,

    -- Configurações SQL Server
    SqlServidor NVARCHAR(255),
    SqlBancoDados NVARCHAR(100),
    SqlUsuario NVARCHAR(100),
    SqlSenha NVARCHAR(255),
    SqlDriver NVARCHAR(255),

    -- Configurações de PDFs
    PdfsCaminho NVARCHAR(500),

    -- Configurações de Email - SMTP
    EmailSmtpServidor NVARCHAR(255),
    EmailSmtpPorta INT,
    EmailUsuario NVARCHAR(255),
    EmailSenhaApp NVARCHAR(255),
    EmailRemetente NVARCHAR(255),

    -- Configurações de Email - Templates ⭐ NOVO
    EmailAssunto NVARCHAR(500),
    EmailCorpo NVARCHAR(MAX),

    -- Configurações do Sistema
    SistemaVerificacaoInicial BIT,
    SistemaAguardarSegundosAposArquivo INT,
    SistemaVerificacaoPeriodicaAtiva BIT,
    SistemaVerificacaoPeriodicaMinutos INT,

    -- Configurações de Cool-down
    SistemaCooldownTentativa1 INT,
    SistemaCooldownTentativa2 INT,
    SistemaCooldownTentativa3 INT,
    SistemaCooldownTentativa4 INT,
    SistemaCooldownTentativa5Mais INT,

    -- Controle
    Ativo BIT DEFAULT 1,
    DataCriacao DATETIME DEFAULT GETDATE(),
    DataAlteracao DATETIME,
    UsuarioAlteracao NVARCHAR(100),
    Observacoes NVARCHAR(MAX)
);
```

---

## 🚀 Como Instalar

### Passo 1: Executar o Script SQL

Execute o arquivo `criar_tabela_configuracoes.sql` no seu banco de dados SRPP:

```bash
# Via SQL Server Management Studio (SSMS)
# Ou via linha de comando:
sqlcmd -S 127.0.0.1 -U sa -P M4573R -d SRPP -i criar_tabela_configuracoes.sql
```

O script irá:
1. Criar a tabela `ConfiguracaoSistema`
2. Inserir um registro padrão com as configurações atuais
3. Marcar esse registro como `Ativo = 1`

### Passo 2: Verificar a Configuração

```sql
SELECT * FROM ConfiguracaoSistema WHERE Ativo = 1;
```

### Passo 3: Reiniciar o Sistema

```bash
python sender.py
```

O sistema irá:
1. Tentar conectar ao banco usando `config.ini` (apenas para conexão inicial)
2. Carregar todas as configurações da tabela `ConfiguracaoSistema`
3. Usar as configurações do banco para todo o funcionamento
4. Fazer fallback para `config.ini` se o banco estiver indisponível

---

## 🎨 Templates de Email Parametrizáveis

### Variáveis Disponíveis

Você pode usar as seguintes variáveis nos campos `EmailAssunto` e `EmailCorpo`:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{NroPedido}` | Número do pedido | `0000123` |
| `{RazaoSocial}` | Nome do cliente | `João da Silva` |
| `{DataPedidoFechado}` | Data do fechamento | `25/12/2024` |
| `{VersaoPdf}` | Versão do PDF | `1`, `2`, `3`... |
| `{MensagemReenvio}` | Mensagem automática de reenvio | *(vazio ou texto)* |

### Exemplo de Assunto

```
Pedido {NroPedido} - {RazaoSocial}
```

**Resultado:**
```
Pedido 0000123 - João da Silva
```

### Exemplo de Corpo

```
Prezado(a) {RazaoSocial},

Segue em anexo o PDF do seu pedido número {NroPedido}, fechado em {DataPedidoFechado}.

{MensagemReenvio}

Qualquer dúvida, estamos à disposição.

Atenciosamente,
Equipe SRPP
Sistema Automatizado de Envio
```

**Resultado (primeiro envio):**
```
Prezado(a) João da Silva,

Segue em anexo o PDF do seu pedido número 0000123, fechado em 25/12/2024.



Qualquer dúvida, estamos à disposição.

Atenciosamente,
Equipe SRPP
Sistema Automatizado de Envio
```

**Resultado (reenvio - versão 2):**
```
Prezado(a) João da Silva,

Segue em anexo o PDF do seu pedido número 0000123, fechado em 25/12/2024.

ATENÇÃO: Esta é uma versão atualizada do pedido (versão 2).
Esta versão substitui a anterior.

Qualquer dúvida, estamos à disposição.

Atenciosamente,
Equipe SRPP
Sistema Automatizado de Envio
```

---

## 📝 Como Atualizar Configurações

### Atualizar Assunto do Email

```sql
UPDATE ConfiguracaoSistema
SET EmailAssunto = 'Novo Pedido #{NroPedido} - {RazaoSocial}',
    DataAlteracao = GETDATE(),
    UsuarioAlteracao = 'Admin'
WHERE Ativo = 1;
```

### Atualizar Corpo do Email

```sql
UPDATE ConfiguracaoSistema
SET EmailCorpo = 'Olá {RazaoSocial},

Seu pedido {NroPedido} está pronto!

{MensagemReenvio}

Att,
Sistema SRPP',
    DataAlteracao = GETDATE(),
    UsuarioAlteracao = 'Admin'
WHERE Ativo = 1;
```

### Atualizar Credenciais de Email

```sql
UPDATE ConfiguracaoSistema
SET EmailUsuario = 'novo_email@gmail.com',
    EmailSenhaApp = 'nova_senha_app',
    DataAlteracao = GETDATE()
WHERE Ativo = 1;
```

### Atualizar Caminho de PDFs

```sql
UPDATE ConfiguracaoSistema
SET PdfsCaminho = 'D:\NovaPasta\PDFs',
    DataAlteracao = GETDATE()
WHERE Ativo = 1;
```

### Atualizar Configurações de Cool-down

```sql
UPDATE ConfiguracaoSistema
SET SistemaCooldownTentativa1 = 5,
    SistemaCooldownTentativa2 = 10,
    SistemaCooldownTentativa3 = 15,
    DataAlteracao = GETDATE()
WHERE Ativo = 1;
```

**⚠️ IMPORTANTE:** Após atualizar as configurações no banco, **reinicie o sistema** para aplicar as mudanças.

---

## 🔄 Sistema de Fallback

O sistema possui **fallback automático** para garantir disponibilidade:

### Fluxo de Carregamento de Configurações

```
1. Sistema inicia
   ↓
2. Carrega config.ini (APENAS credenciais de conexão SQL)
   ↓
3. Conecta ao banco de dados SQL Server
   ↓
4. Busca configurações na tabela ConfiguracaoSistema (WHERE Ativo = 1)
   ↓
5. Se encontrou configuração ativa:
   → Usa configurações DO BANCO para tudo
   ↓
6. Se NÃO encontrou ou erro de conexão:
   → Usa config.ini como FALLBACK
   → Loga warning no arquivo de log
```

### Exemplos de Fallback

**Cenário 1: Banco disponível e tabela existe**
```
✅ Configurações carregadas do banco de dados com sucesso!
```

**Cenário 2: Banco indisponível**
```
⚠️ Não foi possível conectar ao banco para carregar configurações. Usando config.ini como fallback.
```

**Cenário 3: Tabela não existe**
```
⚠️ Erro ao carregar configurações do banco: Invalid object name 'ConfiguracaoSistema'. Usando config.ini como fallback.
```

**Cenário 4: Nenhuma configuração ativa**
```
⚠️ Nenhuma configuração ativa encontrada na tabela ConfiguracaoSistema. Usando config.ini como fallback.
```

---

## 🔒 Segurança

### Antes (config.ini)
```ini
[SQL_SERVER]
usuario = sa
senha = M4573R

[EMAIL]
senha_app = tgszqnhvpsauzuhl
```
- ❌ Credenciais em texto plano no disco
- ❌ Arquivo facilmente copiado
- ❌ Visível em backups de código

### Agora (Banco de Dados)
```sql
SELECT SqlSenha, EmailSenhaApp FROM ConfiguracaoSistema WHERE Ativo = 1;
```
- ✅ Credenciais dentro do banco de dados
- ✅ Controle de acesso do SQL Server
- ✅ Possibilidade de criptografia futura
- ✅ Auditoria de alterações

---

## 📊 Gerenciamento de Múltiplas Configurações

Você pode ter **múltiplas configurações** salvas, mas apenas **uma ativa por vez**.

### Criar Nova Configuração (Produção)

```sql
INSERT INTO ConfiguracaoSistema (
    SqlServidor, SqlBancoDados, SqlUsuario, SqlSenha, SqlDriver,
    PdfsCaminho, EmailSmtpServidor, EmailSmtpPorta,
    EmailUsuario, EmailSenhaApp, EmailRemetente,
    EmailAssunto, EmailCorpo,
    Ativo, Observacoes
) VALUES (
    '192.168.1.100', 'SRPP_PRODUCAO', 'sa_prod', 'senha_prod', 'ODBC Driver 17 for SQL Server',
    'E:\Producao\PDFs', 'smtp.gmail.com', 587,
    'producao@empresa.com', 'senha_prod_gmail', 'Sistema SRPP Produção',
    'Pedido {NroPedido} - {RazaoSocial}',
    'Prezado(a) {RazaoSocial}...',
    0, -- Não ativa por enquanto
    'Configuração de produção'
);
```

### Alternar Configurações

```sql
-- Desativar configuração atual
UPDATE ConfiguracaoSistema SET Ativo = 0 WHERE Ativo = 1;

-- Ativar nova configuração (ex: ID = 2)
UPDATE ConfiguracaoSistema SET Ativo = 1 WHERE Id = 2;
```

---

## 🧪 Testando

### Teste 1: Verificar Carregamento

```bash
python sender.py
```

Verifique nos logs:
```
✅ Configurações carregadas do banco de dados com sucesso!
```

### Teste 2: Modo Teste (sem enviar emails)

```bash
python sender.py --teste
```

### Teste 3: Atualizar Template e Testar

```sql
UPDATE ConfiguracaoSistema
SET EmailAssunto = 'TESTE - Pedido {NroPedido}'
WHERE Ativo = 1;
```

Reinicie o sistema e processe um pedido de teste.

---

## 🐛 Troubleshooting

### Problema: Sistema não carrega configurações do banco

**Sintoma:**
```
⚠️ Não foi possível conectar ao banco para carregar configurações. Usando config.ini como fallback.
```

**Solução:**
1. Verifique se o banco está acessível
2. Verifique credenciais no `config.ini`
3. Execute o script `criar_tabela_configuracoes.sql`

### Problema: Variáveis não são substituídas no email

**Sintoma:**
Assunto do email aparece como: `Pedido {NroPedido} - {RazaoSocial}`

**Solução:**
1. Verifique se as configurações foram carregadas do banco
2. Procure no log por: `Configurações carregadas do banco de dados com sucesso!`
3. Se não aparecer, o sistema está usando templates padrão antigos

### Problema: Erro ao inserir configuração

**Sintoma:**
```
Violation of UNIQUE KEY constraint 'IX_ConfiguracaoSistema_Ativo'
```

**Solução:**
Só pode haver **uma configuração ativa** por vez. Desative a anterior:
```sql
UPDATE ConfiguracaoSistema SET Ativo = 0 WHERE Ativo = 1;
```

---

## 📚 Compatibilidade

### config.ini ainda é necessário?

**Sim**, mas apenas para a **conexão inicial** ao banco de dados.

O sistema precisa do `config.ini` para:
1. ✅ Obter credenciais para conectar ao SQL Server
2. ✅ Funcionar como fallback se o banco estiver indisponível

Após conectar, **todas as outras configurações** vêm do banco.

### Posso remover o config.ini?

**Não recomendado**. O `config.ini` serve como:
- Fallback de emergência
- Bootstrap inicial para conexão
- Documentação de estrutura

---

## 🎓 Próximos Passos

1. ✅ Execute o script SQL: `criar_tabela_configuracoes.sql`
2. ✅ Verifique a configuração: `SELECT * FROM ConfiguracaoSistema WHERE Ativo = 1`
3. ✅ Personalize assunto e corpo do email conforme sua necessidade
4. ✅ Teste o sistema: `python sender.py --teste`
5. ✅ Coloque em produção

---

## 💡 Dicas

- Use `{MensagemReenvio}` no corpo para mensagens automáticas de reenvio
- Deixe uma linha em branco antes de `{MensagemReenvio}` para formatação
- Teste sempre no modo `--teste` antes de produção
- Mantenha um backup das configurações

---

**Versão:** 2.0
**Data:** Dezembro 2024
**Autor:** Sistema EnviaEmailSRPP
