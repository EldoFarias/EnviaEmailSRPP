-- =====================================================
-- Script de Criação da Tabela: ConfiguracaoSistemaEmail
-- Sistema: EnviaEmailSRPP
-- Descrição: Tabela para armazenar configurações do
--            sistema de envio automático de emails
-- =====================================================

USE SRPP;
GO

-- Remove todas as versões incorretas da tabela
IF OBJECT_ID('dbo.ConfiguracaoSistema', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.ConfiguracaoSistema;
    PRINT 'Tabela ConfiguracaoSistema (incorreta) removida.';
END

IF OBJECT_ID('dbo.ConfiguracaoSistemaEmailEmail', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.ConfiguracaoSistemaEmailEmail;
    PRINT 'Tabela ConfiguracaoSistemaEmailEmail (incorreta) removida.';
END

IF OBJECT_ID('dbo.ConfiguracaoSistemaEmail', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.ConfiguracaoSistemaEmail;
    PRINT 'Tabela ConfiguracaoSistemaEmail existente removida.';
END
GO

-- Criação da tabela ConfiguracaoSistemaEmail
CREATE TABLE dbo.ConfiguracaoSistemaEmail (
    -- Chave primária
    Id INT IDENTITY(1,1) PRIMARY KEY,

    -- Configurações SQL Server
    SqlServidor NVARCHAR(255) NOT NULL DEFAULT '127.0.0.1',
    SqlBancoDados NVARCHAR(100) NOT NULL DEFAULT 'SRPP',
    SqlUsuario NVARCHAR(100) NOT NULL,
    SqlSenha NVARCHAR(255) NOT NULL,
    SqlDriver NVARCHAR(255) NOT NULL DEFAULT 'ODBC Driver 17 for SQL Server',

    -- Configurações de PDFs
    PdfsCaminho NVARCHAR(500) NOT NULL,

    -- Configurações de Email - SMTP
    EmailSmtpServidor NVARCHAR(255) NOT NULL,
    EmailSmtpPorta INT NOT NULL DEFAULT 587,
    EmailUsuario NVARCHAR(255) NOT NULL,
    EmailSenhaApp NVARCHAR(255) NOT NULL,
    EmailRemetente NVARCHAR(255) NOT NULL,

    -- Configurações de Email - Templates
    EmailAssunto NVARCHAR(500) NOT NULL DEFAULT 'Pedido {NroPedido} - PDF Anexado',
    EmailCorpo NVARCHAR(MAX) NOT NULL DEFAULT 'Prezado(a) Cliente,

Segue em anexo o PDF do seu pedido {NroPedido}.

Atenciosamente,
Equipe SRPP',
    EmailExpositor NVARCHAR(255) NULL,

    -- Configurações do Sistema
    SistemaVerificacaoInicial BIT NOT NULL DEFAULT 1,
    SistemaAguardarSegundosAposArquivo INT NOT NULL DEFAULT 5,
    SistemaVerificacaoPeriodicaAtiva BIT NOT NULL DEFAULT 1,
    SistemaVerificacaoPeriodicaMinutos INT NOT NULL DEFAULT 30,

    -- Configurações de Cool-down (em minutos)
    SistemaCooldownTentativa1 INT NOT NULL DEFAULT 2,
    SistemaCooldownTentativa2 INT NOT NULL DEFAULT 5,
    SistemaCooldownTentativa3 INT NOT NULL DEFAULT 10,
    SistemaCooldownTentativa4 INT NOT NULL DEFAULT 20,
    SistemaCooldownTentativa5Mais INT NOT NULL DEFAULT 30,

    -- Controle de versão e auditoria
    Ativo BIT NOT NULL DEFAULT 1,
    DataCriacao DATETIME NOT NULL DEFAULT GETDATE(),
    DataAlteracao DATETIME NULL,
    UsuarioAlteracao NVARCHAR(100) NULL,
    Observacoes NVARCHAR(MAX) NULL
);
GO

-- Criar índice único filtrado para garantir apenas um registro ativo
CREATE UNIQUE INDEX IX_ConfiguracaoSistemaEmail_Ativo 
ON dbo.ConfiguracaoSistemaEmail(Ativo) 
WHERE Ativo = 1;
GO

-- Comentários na tabela
EXEC sys.sp_addextendedproperty
    @name=N'MS_Description',
    @value=N'Tabela de configurações do sistema de envio automático de emails. Apenas um registro pode estar ativo por vez.',
    @level0type=N'SCHEMA', @level0name=N'dbo',
    @level1type=N'TABLE', @level1name=N'ConfiguracaoSistemaEmail';
GO

-- Inserir configuração padrão
INSERT INTO dbo.ConfiguracaoSistemaEmail (
    SqlServidor, SqlBancoDados, SqlUsuario, SqlSenha, SqlDriver,
    PdfsCaminho,
    EmailSmtpServidor, EmailSmtpPorta, EmailUsuario, EmailSenhaApp, EmailRemetente,
    EmailAssunto, EmailCorpo,
    SistemaVerificacaoInicial, SistemaAguardarSegundosAposArquivo,
    SistemaVerificacaoPeriodicaAtiva, SistemaVerificacaoPeriodicaMinutos,
    SistemaCooldownTentativa1, SistemaCooldownTentativa2, SistemaCooldownTentativa3,
    SistemaCooldownTentativa4, SistemaCooldownTentativa5Mais,
    Ativo, Observacoes
) VALUES (
    '127.0.0.1', 'SRPP', 'sa', 'M4573R', 'ODBC Driver 17 for SQL Server',
    'C:\Users\Public\Documents\SRPP\PDFs',
    'smtp.gmail.com', 587, 'eldofarias81@gmail.com', 'tgszqnhvpsauzuhl', 'Sistema SRPP',
    'Pedido {NroPedido} - {RazaoSocial}',
    'Prezado(a) {RazaoSocial},

Segue em anexo o PDF do seu pedido número {NroPedido}, fechado em {DataPedidoFechado}.

{MensagemReenvio}

Qualquer dúvida, estamos à disposição.

Atenciosamente,
Equipe SRPP
Sistema Automatizado de Envio',
    1, 5, 1, 30,
    2, 5, 10, 20, 30,
    1, 'Configuração inicial migrada do config.ini'
);
GO

PRINT '=================================================';
PRINT 'Tabela ConfiguracaoSistemaEmail criada com sucesso!';
PRINT 'Registro padrão inserido.';
PRINT '=================================================';
PRINT '';
PRINT 'VARIÁVEIS DISPONÍVEIS PARA TEMPLATES:';
PRINT '- {NroPedido}: Número do pedido';
PRINT '- {RazaoSocial}: Nome do cliente';
PRINT '- {DataPedidoFechado}: Data que o pedido foi fechado';
PRINT '- {MensagemReenvio}: Mensagem automática de reenvio (se aplicável)';
PRINT '- {VersaoPdf}: Versão do PDF (1, 2, 3...)';
PRINT '- {EmailExpositor}: Email do expositor (configurado na tabela ConfiguracaoSistemaEmail)';
PRINT '- {EmailRepresentante}: Email do representante do pedido';
PRINT '';
PRINT 'EXEMPLO DE CONSULTA:';
PRINT 'SELECT * FROM ConfiguracaoSistemaEmail WHERE Ativo = 1;';
GO