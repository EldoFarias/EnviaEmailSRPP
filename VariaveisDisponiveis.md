# 📋 Variáveis Disponíveis para Templates de Email

Este documento lista **todas as variáveis** que podem ser usadas na construção do **Assunto** (`EmailAssunto`) e do **Corpo** (`EmailCorpo`) do email, configurados na tabela `ConfiguracaoSistemaEmail`.

Para usar uma variável, escreva o nome dela entre chaves: `{NomeVariavel}`

---

## 📦 Variáveis do Pedido

| Variável | Descrição | Exemplo |
|---|---|---|
| `{NroPedido}` | Número do pedido | `0001234` |
| `{RazaoSocial}` | Nome/Razão Social do cliente | `Empresa ABC Ltda` |
| `{DataPedidoFechado}` | Data em que o pedido foi fechado | `15/03/2025` |
| `{VersaoPdf}` | Versão do PDF anexo (1, 2, 3...) | `1` |
| `{MensagemReenvio}` | Texto automático quando é um reenvio de versão atualizada. **Vazio no primeiro envio.** | `ATENÇÃO: Esta é uma versão atualizada...` |

---

## 📧 Variáveis de Email

| Variável | Descrição | Exemplo |
|---|---|---|
| `{EmailReplyTo}` | Endereço de resposta configurado em `EmailResponderPara` | `atendimento@empresa.com.br` |
| `{ResponderPara}` | Mesmo que `{EmailReplyTo}` (alias) | `atendimento@empresa.com.br` |
| `{EmailExpositor}` | Email do expositor, configurado no campo `EmailExpositor` da tabela `ConfiguracaoSistemaEmail`. **Vazio se não configurado.** | `expositor@empresa.com.br` |
| `{EmailRepresentante}` | Email do representante vinculado ao pedido (buscado automaticamente na tabela `Representante`). **Vazio se o pedido não tiver representante.** | `rep.joao@empresa.com.br` |

---

## 🎨 Variáveis de Estilo (HTML)

| Variável | Descrição | Valor padrão |
|---|---|---|
| `{HeaderColor}` | Cor do cabeçalho em formato hexadecimal (útil em templates HTML) | `#0a77d5` |

---

## 📝 Como Usar

### Exemplo — Assunto simples:
```
Pedido {NroPedido} - {RazaoSocial}
```
**Resultado:** `Pedido 0001234 - Empresa ABC Ltda`

---

### Exemplo — Corpo em TEXTO:
```
Prezado(a) {RazaoSocial},

Segue em anexo o PDF do seu pedido número {NroPedido},
fechado em {DataPedidoFechado}.

{MensagemReenvio}

Qualquer dúvida, estamos à disposição.

Atenciosamente,
Equipe SRPP
```

---

### Exemplo — Corpo em HTML:

> Para usar HTML, a **primeira linha** do corpo deve ser exatamente `#HTML`

```
#HTML
<html>
<body style="font-family: Arial, sans-serif;">

  <div style="background-color: {HeaderColor}; padding: 20px;">
    <h2 style="color: white;">Pedido {NroPedido}</h2>
  </div>

  <div style="padding: 20px;">
    <p>Prezado(a) <strong>{RazaoSocial}</strong>,</p>
    <p>Segue em anexo o PDF do seu pedido número <strong>{NroPedido}</strong>,
    fechado em <strong>{DataPedidoFechado}</strong>.</p>

    {MensagemReenvio}

    <p>Atenciosamente,<br>Equipe SRPP</p>
  </div>

</body>
</html>
```

---

### Exemplo — Corpo em TEXTO (forçado explícito):

> Para forçar texto simples, a **primeira linha** pode ser `#TEXTO`

```
#TEXTO
Prezado(a) {RazaoSocial},

Pedido: {NroPedido}
Data: {DataPedidoFechado}
Versão do PDF: {VersaoPdf}

{MensagemReenvio}

Atenciosamente,
Equipe SRPP
```

---

## 🔁 Comportamento do `{MensagemReenvio}`

- **Primeiro envio:** a variável é substituída por uma string **vazia** — não aparece nada.
- **Reenvio (versão atualizada):** a variável é substituída automaticamente pela mensagem:
  - **TEXTO:** `ATENÇÃO: Esta é uma versão atualizada do pedido (versão X). Esta versão substitui a anterior.`
  - **HTML:** `<strong>ATENÇÃO:</strong> Esta é uma versão atualizada do pedido (versão X).<br>Esta versão substitui a anterior.`

> **Dica:** Deixe uma linha em branco antes e depois de `{MensagemReenvio}` para o texto ficar bem espaçado quando aparecer.

---

## ✉️ Destinatários automáticos (CC)

As variáveis abaixo determinam **quem recebe cópia** do email automaticamente. Elas não precisam estar no template para funcionar — o sistema já inclui os endereços no CC se estiverem preenchidos:

| Campo | Origem | Comportamento |
|---|---|---|
| `EmailExpositor` | Tabela `ConfiguracaoSistemaEmail` | Adicionado ao CC se preenchido e válido |
| `EmailRepresentante` | Tabela `Representante` via `CabecalhoPedido` | Adicionado ao CC se o pedido tiver representante com email válido |
| `EmailsCopia` | Tabela `ControleEmailPedidos` | Campo de cópias manuais por pedido |

> Emails duplicados são removidos automaticamente — o mesmo endereço nunca aparece duas vezes.

---

## ⚠️ Observações Importantes

1. **Case sensitive:** os nomes das variáveis diferenciam maiúsculas de minúsculas. Use exatamente como documentado. Ex: `{NroPedido}` ✅ — `{nropedido}` ❌
2. **Chaves literais no HTML:** se precisar usar `{` ou `}` no template sem ser variável, duplique: `{{` e `}}`
3. **Variáveis vazias:** variáveis sem valor (ex: `{MensagemReenvio}` no primeiro envio) são substituídas por string vazia — não causam erro.
4. **Tipo do conteúdo:** se o corpo **não** começar com `#HTML` ou `#TEXTO`, o sistema trata como **texto simples** por padrão.

---

**Última atualização:** 2026-03-03
**Dúvidas:** Consulte `README.md` ou `INSTALACAO.md`
