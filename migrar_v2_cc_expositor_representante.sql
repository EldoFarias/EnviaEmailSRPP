-- =====================================================
-- Script de Migração: Adiciona EmailExpositor à tabela ConfiguracaoSistemaEmail
-- Sistema: EnviaEmailSRPP
-- Versão: 2.x - Suporte a CC automático para Expositor e Representante
-- Descrição: Execute este script em instalações existentes para adicionar
--            o campo EmailExpositor sem recriar a tabela.
-- =====================================================

USE SRPP;
GO

-- Adiciona a coluna EmailExpositor se ainda não existir
IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'ConfiguracaoSistemaEmail'
      AND COLUMN_NAME = 'EmailExpositor'
)
BEGIN
    ALTER TABLE dbo.ConfiguracaoSistemaEmail
    ADD EmailExpositor NVARCHAR(255) NULL;

    PRINT 'Coluna EmailExpositor adicionada com sucesso.';
END
ELSE
BEGIN
    PRINT 'Coluna EmailExpositor já existe. Nenhuma alteração necessária.';
END
GO

PRINT '=================================================';
PRINT 'Migração concluída!';
PRINT '';
PRINT 'Para configurar o email do expositor, execute:';
PRINT 'UPDATE ConfiguracaoSistemaEmail';
PRINT '   SET EmailExpositor = ''expositor@exemplo.com.br''';
PRINT ' WHERE Ativo = 1;';
PRINT '';
PRINT 'VARIÁVEIS DISPONÍVEIS NOS TEMPLATES (novas):';
PRINT '- {EmailExpositor}: Email do expositor configurado nesta tabela';
PRINT '- {EmailRepresentante}: Email do representante vinculado ao pedido';
PRINT '=================================================';
GO
