#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste rápido de autenticação SMTP
"""

import smtplib
import sys

def testar_smtp(email, senha):
    """Testa autenticação SMTP do Gmail"""
    print("=" * 60)
    print("TESTE DE AUTENTICAÇÃO SMTP - GMAIL")
    print("=" * 60)
    print(f"\nEmail: {email}")
    print(f"Senha App: {senha[:4]}{'*' * (len(senha) - 4)}")
    print("\nTestando conexão...\n")

    try:
        # Conectar ao servidor Gmail
        print("1. Conectando ao smtp.gmail.com:587...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        print("   [OK] Conectado com sucesso!\n")

        # Iniciar TLS
        print("2. Iniciando conexao segura TLS...")
        server.starttls()
        print("   [OK] TLS ativado!\n")

        # Tentar autenticar
        print("3. Tentando autenticar...")
        server.login(email, senha)
        print("   [OK] AUTENTICACAO BEM-SUCEDIDA!\n")

        # Fechar conexão
        server.quit()

        print("=" * 60)
        print("[OK] TESTE CONCLUIDO COM SUCESSO!")
        print("=" * 60)
        print("\nAs credenciais estao corretas e funcionando.")
        print("O email pode ser enviado normalmente com essas configuracoes.\n")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print("   [ERRO] ERRO DE AUTENTICACAO!\n")
        print("=" * 60)
        print("[ERRO] FALHA NA AUTENTICACAO")
        print("=" * 60)
        print("\nPossiveis causas:")
        print("1. Senha de app incorreta ou invalida")
        print("2. Senha de app foi revogada no Google")
        print("3. Email nao tem autenticacao de 2 fatores ativada")
        print("4. Email/senha digitados com espacos extras")
        print("5. Dominio sint.com.br nao esta configurado corretamente no Google Workspace")
        print("\nComo resolver:")
        print("1. Verifique se o dominio sint.com.br esta usando Google Workspace")
        print("2. Se sim, acesse: https://myaccount.google.com/apppasswords")
        print("3. Gere uma nova senha de app")
        print("4. Use a senha de 16 caracteres sem espacos")
        print(f"\nDetalhes do erro: {e}\n")
        return False

    except smtplib.SMTPException as e:
        print("   [ERRO] ERRO SMTP!\n")
        print("=" * 60)
        print("[ERRO] ERRO NO SERVIDOR SMTP")
        print("=" * 60)
        print(f"\nDetalhes: {e}\n")
        return False

    except Exception as e:
        print("   [ERRO] ERRO INESPERADO!\n")
        print("=" * 60)
        print("[ERRO] ERRO INESPERADO")
        print("=" * 60)
        print(f"\nDetalhes: {e}\n")
        return False

if __name__ == "__main__":
    # Credenciais para teste
    email = "eldofarias81@gmail.com"
    senha = "usyhuizdzprbxvkf"

    # Remover espaços da senha (senhas de app do Gmail não tem espaços)
    senha_limpa = senha.replace(" ", "")

    print("\nNOTA: Removendo espaços da senha de app...")
    print(f"Senha original: '{senha}'")
    print(f"Senha sem espaços: '{senha_limpa}'\n")

    # Testar
    sucesso = testar_smtp(email, senha_limpa)

    sys.exit(0 if sucesso else 1)
