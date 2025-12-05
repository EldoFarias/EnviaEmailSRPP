#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste completo SMTP para Gmail, Outlook, Office365 e servidores comuns
"""

import smtplib
import ssl
import sys

# Lista de servidores para testar
SERVIDORES = [
    {"nome": "Gmail", "host": "smtp.gmail.com", "port": 587, "ssl": False},
    {"nome": "Gmail SSL", "host": "smtp.gmail.com", "port": 465, "ssl": True},

    {"nome": "Outlook/Hotmail/Office365", "host": "smtp.office365.com", "port": 587, "ssl": False},
    {"nome": "Outlook SSL", "host": "smtp-mail.outlook.com", "port": 465, "ssl": True},

    # SMTP genéricos comuns
    {"nome": "SMTP Genérico TLS", "host": None, "port": 587, "ssl": False},
    {"nome": "SMTP Genérico SSL", "host": None, "port": 465, "ssl": True},
]

def testar(email, senha, host, port, usar_ssl):
    print(f"\n=== Testando {host}:{port} / SSL={usar_ssl} ===")

    try:
        if usar_ssl:
            contexto = ssl.create_default_context()
            server = smtplib.SMTP_SSL(host, port, context=contexto)
        else:
            server = smtplib.SMTP(host, port)
            server.starttls()

        server.login(email, senha)
        server.quit()

        print(f"[SUCESSO] Autenticado com sucesso em {host}:{port} (SSL={usar_ssl})")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"[ERRO] Falha de autenticação: {e}")
        return False

    except Exception as e:
        print(f"[ERRO] Não conectou ou falhou: {e}")
        return False


if __name__ == "__main__":
    # PREENCHA AQUI
    email = "nao-responda@sint.com.br"
    senha = "vdvmnfblzxvccqhw"

    dominio = email.split("@")[1]

    print("\n################################################")
    print(" INICIANDO TESTE COMPLETO DE SERVIDORES SMTP")
    print("################################################")
    print(f"E-mail: {email}")
    print(f"Dominio detectado: {dominio}")
    print("------------------------------------------------\n")

    senha = senha.replace(" ", "")

    for srv in SERVIDORES:
        host = srv["host"] if srv["host"] else f"smtp.{dominio}"
        testar(email, senha, host, srv["port"], srv["ssl"])

    print("\n################################################")
    print(" TESTE FINALIZADO")
    print("################################################\n")

    sys.exit(0)
