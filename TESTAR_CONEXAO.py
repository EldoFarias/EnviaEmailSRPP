#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

def testar_send_as(usuario_login, senha, remetente_fake, destinatario_teste):
    print("\n" + "="*60)
    print(" TESTE DE ENVIO SEND-AS (Office365)")
    print("="*60)
    print(f"Autenticando como: {usuario_login}")
    print(f"Tentando enviar COMO: {remetente_fake}")
    print(f"Destino do teste: {destinatario_teste}\n")

    try:
        # Conectar ao servidor SMTP
        print("[1] Conectando ao servidor SMTP...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.ehlo()
        print("   ✔ OK conectado!")

        # TLS
        print("[2] Iniciando TLS...")
        server.starttls()
        server.ehlo()
        print("   ✔ TLS estabelecido!")

        # Login
        print("[3] Autenticando...")
        server.login(usuario_login, senha)
        print("   ✔ Autenticado com sucesso!\n")

        # Criar email
        print("[4] Preparando email para envio...")
        msg = MIMEText("Teste automático SEND AS para validar permissões.\n", "plain", "utf-8")
        msg['Subject'] = Header("Teste SEND AS - Office365", "utf-8")
        msg['From'] = remetente_fake
        msg['To'] = destinatario_teste

        # Tentar enviar
        print("[5] Enviando email...")
        server.sendmail(remetente_fake, destinatario_teste, msg.as_string())
        print("\n   ✔ EMAIL ENVIADO COM SUCESSO!")
        print("   ✔ Permissão SEND-AS funcionando corretamente!\n")

        server.quit()
        return True

    except smtplib.SMTPAuthenticationError as e:
        print("\n   ✖ ERRO: Falha de autenticação")
        print("   Detalhes:", e)
        print("\nPossíveis causas:")
        print("- Senha incorreta")
        print("- MFA/Habilitação de segurança bloqueando")
        print("- Política de app password necessária")
        return False

    except smtplib.SMTPRecipientsRefused as e:
        print("\n   ✖ ERRO: Destinatário rejeitado")
        print("   Detalhes:", e)
        return False

    except smtplib.SMTPSenderRefused as e:
        print("\n   ✖ ERRO: O servidor REJEITOU o remetente (FROM)")
        print("   Isso significa 100% que o usuário NÃO TEM permissão SEND AS.")
        print("   Detalhes:", e)
        return False

    except smtplib.SMTPException as e:
        print("\n   ✖ ERRO SMTP:")
        print("   Detalhes:", e)
        return False

    except Exception as e:
        print("\n   ✖ ERRO INESPERADO:")
        print("   Detalhes:", e)
        return False


if __name__ == "__main__":
    # Preencha aqui
    usuario_login = "eldo@sint.com.br"     # Usuário que faz login
    senha = "vdvmnfblzxvccqhw"               # Senha da conta ou senha do app
    remetente_fake = "nao-responda@sint.com.br"  # Remetente que você quer usar
    destinatario_teste = "eldo@sint.com.br"  # Pode ser qualquer email
    testar_send_as(usuario_login, senha, remetente_fake, destinatario_teste)
    
    print("\n-------------------------------------------")
    print("Teste finalizado.")
    print("A janela será fechada ao pressionar ENTER.")
    input()

