#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Envio Automático de PDFs por Email
Monitora pasta de PDFs e processa automaticamente quando novos arquivos são criados
"""

import os
import re
import glob
import smtplib
import logging
import pyodbc
import configparser
import time
import signal
import sys
import hashlib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# Para logs em Excel
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
    from openpyxl.utils import get_column_letter
    EXCEL_DISPONIVEL = True
except ImportError:
    EXCEL_DISPONIVEL = False

# Para monitoramento de arquivos
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SistemaEnvioEmails:
    def __init__(self, config_path='config.ini'):
        """Inicializa o sistema com configurações"""
        self.config = self.carregar_configuracoes(config_path)
        self.setup_logging()
        self.conexao_db = None
        self.excel_logger = None
        self.setup_excel_logging()
        
    def carregar_configuracoes(self, config_path):
        """Carrega configurações do arquivo INI"""
        config = configparser.ConfigParser()
        
        config_default = r"""
[SQL_SERVER]
servidor = 127.0.0.1
banco_de_dados = SRPP
usuario = sa
senha = M4573R
driver = ODBC Driver 17 for SQL Server

[PDFS]
caminho = C:\Users\Public\Documents\SRPP\PDFs

[EMAIL]
smtp_servidor = smtp-mail.outlook.com
smtp_porta = 587
usuario = seu_email@empresa.com
senha_app = sua_senha_app_aqui
remetente_nome = Sistema de Vendas

[SISTEMA]
verificacao_inicial = True
aguardar_segundos_apos_arquivo = 5
verificacao_periodica_ativa = True
verificacao_periodica_minutos = 10
max_tentativas = DESABILITADO_USA_COOLDOWN
cooldown_tentativa_1 = 2
cooldown_tentativa_2 = 5
cooldown_tentativa_3 = 10
cooldown_tentativa_4 = 20
cooldown_tentativa_5_mais = 30
"""
        
        if not os.path.exists(config_path):
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(config_default)
            print(f"Arquivo {config_path} criado. Configure suas credenciais e execute novamente.")
            exit(1)
            
        config.read(config_path, encoding='utf-8')
        return config
        
    def setup_logging(self):
        """Configura sistema de logs"""
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/envio_emails.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_excel_logging(self):
        """Configura sistema de logs em Excel"""
        if not EXCEL_DISPONIVEL:
            self.logger.warning("openpyxl não disponível - logs em Excel desabilitados")
            return

        try:
            self.excel_logger = ExcelLogger()
            self.logger.info("Sistema de logs Excel iniciado")
        except Exception as e:
            self.logger.error(f"Erro ao inicializar logs Excel: {e}")
            self.excel_logger = None

    def listar_drivers_odbc_disponiveis(self):
        """Lista todos os drivers ODBC instalados no sistema"""
        try:
            drivers = pyodbc.drivers()
            self.logger.info(f"Drivers ODBC instalados no sistema: {len(drivers)}")
            for driver in drivers:
                self.logger.info(f"  - {driver}")
            return drivers
        except Exception as e:
            self.logger.error(f"Erro ao listar drivers ODBC: {e}")
            return []
        
    def conectar_banco(self):
        """Estabelece conexão com SQL Server com fallback automático de drivers"""
        # Lista de drivers ODBC em ordem de preferência (mais recente para mais antigo)
        drivers_disponiveis = [
            self.config['SQL_SERVER']['driver'],  # Driver configurado pelo usuário (prioridade)
            'ODBC Driver 18 for SQL Server',
            'ODBC Driver 17 for SQL Server',
            'ODBC Driver 13.1 for SQL Server',
            'ODBC Driver 13 for SQL Server',
            'ODBC Driver 11 for SQL Server',
            'SQL Server Native Client 11.0',
            'SQL Server Native Client 10.0',
            'SQL Server',
        ]

        # Remove duplicatas mantendo a ordem
        drivers_unicos = []
        for driver in drivers_disponiveis:
            if driver not in drivers_unicos:
                drivers_unicos.append(driver)

        erros_tentativas = []

        for driver in drivers_unicos:
            try:
                conn_str = (
                    f"DRIVER={{{driver}}};"
                    f"SERVER={self.config['SQL_SERVER']['servidor']};"
                    f"DATABASE={self.config['SQL_SERVER']['banco_de_dados']};"
                    f"UID={self.config['SQL_SERVER']['usuario']};"
                    f"PWD={self.config['SQL_SERVER']['senha']};"
                )
                self.conexao_db = pyodbc.connect(conn_str)
                self.logger.info(f"Conectado ao banco de dados com sucesso usando driver: {driver}")

                # Se conectou com driver diferente do configurado, avisar
                if driver != self.config['SQL_SERVER']['driver']:
                    self.logger.warning(f"Driver configurado '{self.config['SQL_SERVER']['driver']}' não disponível. Usando '{driver}' como alternativa.")

                return True

            except Exception as e:
                erros_tentativas.append(f"{driver}: {str(e)[:100]}")
                # Continua tentando próximo driver

        # Se chegou aqui, nenhum driver funcionou
        self.logger.error("ERRO: Não foi possível conectar ao banco de dados com nenhum driver ODBC disponível")
        self.logger.error("Drivers tentados:")
        for erro in erros_tentativas:
            self.logger.error(f"  - {erro}")
        self.logger.error("SOLUÇÃO: Instale um driver ODBC para SQL Server:")
        self.logger.error("  - Download: https://go.microsoft.com/fwlink/?linkid=2249004")

        return False
            
    def buscar_pedidos_para_processar(self):
        """Busca todos os pedidos que precisam ser processados"""
        query = """
        SELECT
            cep.Id, cep.NroPedido, cep.CodCliente, cep.DataPedidoFechado, cep.EmailsCopia,
            c.EMAIL as EmailCliente, c.NomeContato as NomeCliente,
            cep.VersaoPdfEnviada, cep.StatusProcessamento, cep.EmailEnviado,
            cep.TentativasEnvio, NULL as DataUltimaVerificacao, cep.UltimoErro,
            cep.EnviarEmailCliente
        FROM ControleEmailPedidos cep
        INNER JOIN CabecalhoPedido cap ON cap.NroPedido = cep.NroPedido
        INNER JOIN Cliente c ON c.CodCliente = cap.CodCliente
        WHERE cap.SituacaoAtual = 'F'
            AND (
                (cep.StatusProcessamento = 'PENDENTE' AND cep.EmailEnviado = 0) OR
                (cep.StatusProcessamento = 'ENVIADO' AND cep.EmailEnviado = 1) OR
                (cep.StatusProcessamento = 'ERRO_VALIDACAO' AND cep.EmailEnviado = 0) OR
                (cep.StatusProcessamento = 'INVALIDO' AND cep.EmailEnviado = 0)
            )
        ORDER BY cep.DataPedidoFechado
        """
        
        try:
            cursor = self.conexao_db.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            pedidos_para_processar = []
            
            for row in resultados:
                numero_pedido = row.NroPedido
                versao_enviada = int(row.VersaoPdfEnviada) if row.VersaoPdfEnviada is not None else 0
                status_atual = row.StatusProcessamento

                caminho_pdf, versao_disponivel = self.buscar_pdf_pedido(numero_pedido)

                deve_processar = False
                motivo = ""

                if not caminho_pdf:
                    self.logger.warning(f"Pedido {numero_pedido}: PDF não encontrado, pulando...")
                    continue
                elif status_atual in ('PENDENTE', 'INVALIDO') and row.EmailEnviado == 0:
                    deve_processar = True
                    motivo = "PRIMEIRO_ENVIO"
                elif status_atual == 'ENVIADO' and versao_disponivel > versao_enviada:
                    deve_processar = True
                    motivo = "REENVIO_VERSAO_ATUALIZADA"
                elif status_atual == 'ERRO_VALIDACAO' and row.EmailEnviado == 0:
                    deve_processar = True
                    motivo = "REVALIDACAO_APOS_ERRO"
                
                if deve_processar:
                    pedidos_para_processar.append({
                        'id': row.Id, 'numero': numero_pedido, 'cod_cliente': row.CodCliente,
                        'data_fechamento': row.DataPedidoFechado, 'emails_copia': row.EmailsCopia,
                        'email_cliente': row.EmailCliente, 'nome_cliente': row.NomeCliente,
                        'versao_pdf_enviada': versao_enviada, 'status_atual': status_atual,
                        'versao_disponivel': versao_disponivel, 'motivo_processamento': motivo,
                        'caminho_pdf': caminho_pdf, 'tentativas_anteriores': row.TentativasEnvio or 0,
                        'ultimo_erro': row.UltimoErro, 'enviar_email_cliente': row.EnviarEmailCliente
                    })
                    
            self.logger.info(f"Encontrados {len(pedidos_para_processar)} pedidos para processar")
            return pedidos_para_processar
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar pedidos para processar: {e}")
            return []
            
    def _calcular_cooldown(self, tentativas):
        """Calcula tempo de cool-down progressivo"""
        try:
            if tentativas <= 1: return int(self.config.get('SISTEMA', 'cooldown_tentativa_1', fallback=2))
            elif tentativas == 2: return int(self.config.get('SISTEMA', 'cooldown_tentativa_2', fallback=5))
            elif tentativas == 3: return int(self.config.get('SISTEMA', 'cooldown_tentativa_3', fallback=10))
            elif tentativas == 4: return int(self.config.get('SISTEMA', 'cooldown_tentativa_4', fallback=20))
            else: return int(self.config.get('SISTEMA', 'cooldown_tentativa_5_mais', fallback=30))
        except:
            if tentativas <= 1: return 2
            elif tentativas == 2: return 5
            elif tentativas == 3: return 10
            elif tentativas == 4: return 20
            else: return 30
        
    def buscar_pdf_pedido(self, numero_pedido):
        """Busca e identifica a versão mais recente do PDF"""
        caminho_pdfs = self.config['PDFS']['caminho']
        padrao = f"PEDIDO {str(numero_pedido).zfill(7)}*.pdf"
        arquivos = glob.glob(os.path.join(caminho_pdfs, padrao))
        
        if not arquivos:
            self.logger.warning(f"Nenhum PDF encontrado para pedido {numero_pedido}")
            return None, 0
            
        versao_maxima = 1
        arquivo_mais_recente = None
        for arquivo in arquivos:
            match = re.search(r'PEDIDO \d+(?:_(\d+))?\.pdf$', os.path.basename(arquivo))
            if match:
                versao = int(match.group(1)) if match.group(1) else 1
                if versao >= versao_maxima:
                    versao_maxima = versao
                    arquivo_mais_recente = arquivo
        return arquivo_mais_recente, versao_maxima
        
    def atualizar_status_pedido(self, id_controle, campo, valor, erro=None):
        """Atualiza status do pedido na tabela de controle"""
        try:
            cursor = self.conexao_db.cursor()
            if erro:
                query = f"UPDATE ControleEmailPedidos SET {campo} = ?, UltimoErro = ?, TentativasEnvio = TentativasEnvio + 1 WHERE Id = ?"
                cursor.execute(query, (valor, str(erro)[:500], id_controle))
            else:
                query = f"UPDATE ControleEmailPedidos SET {campo} = ? WHERE Id = ?"
                cursor.execute(query, (valor, id_controle))
            self.conexao_db.commit()
        except Exception as e:
            self.logger.error(f"Erro ao atualizar status do pedido {id_controle}: {e}")
            
    def enviar_email(self, destinatario, nome_cliente, numero_pedido, caminho_pdf, emails_copia=None, eh_reenvio=False, versao_pdf=1, enviar_para_cliente=True):
        """Envia email com PDF anexo"""
        try:
            # Determinar destinatários baseado em enviar_para_cliente
            destinatario_principal = None
            lista_copia = []

            if enviar_para_cliente:
                # Fluxo normal: envia para cliente e cópias
                destinatario_principal = destinatario
                if emails_copia:
                    lista_copia = [email.strip() for email in emails_copia.split(',') if email.strip()]

                if lista_copia:
                    self.logger.info(f"Pedido {numero_pedido}: Enviando PARA cliente ({destinatario}) e CÓPIAS ({len(lista_copia)} email(s): {', '.join(lista_copia)})")
                else:
                    self.logger.info(f"Pedido {numero_pedido}: Enviando apenas PARA cliente ({destinatario}) - Sem emails em cópia")
            else:
                # Fluxo alternativo: envia apenas para emails de cópia
                if emails_copia:
                    lista_emails = [email.strip() for email in emails_copia.split(',') if email.strip()]
                    if lista_emails:
                        destinatario_principal = lista_emails[0]  # Primeiro vai para PARA
                        lista_copia = lista_emails[1:] if len(lista_emails) > 1 else []  # Demais vão para CÓPIAS

                        if lista_copia:
                            self.logger.info(f"Pedido {numero_pedido}: Cliente NÃO receberá email. Enviando PARA ({destinatario_principal}) e CÓPIAS ({len(lista_copia)} email(s): {', '.join(lista_copia)})")
                        else:
                            self.logger.info(f"Pedido {numero_pedido}: Cliente NÃO receberá email. Enviando apenas PARA ({destinatario_principal})")
                    else:
                        self.logger.warning(f"Pedido {numero_pedido}: EnviarEmailCliente=0 e EmailsCopia vazio - Nenhum destinatário definido")
                        return False
                else:
                    self.logger.warning(f"Pedido {numero_pedido}: EnviarEmailCliente=0 e EmailsCopia vazio - Nenhum destinatário definido")
                    return False

            # Montar email
            msg = MIMEMultipart()
            msg['From'] = f"{self.config['EMAIL']['remetente_nome']} <{self.config['EMAIL']['usuario']}>"
            msg['To'] = destinatario_principal
            msg['Subject'] = f"Pedido #{numero_pedido} - {'PDF Atualizado' if eh_reenvio else 'PDF Disponível'}"

            if lista_copia:
                msg['Cc'] = ', '.join(lista_copia)

            data_atual = datetime.now().strftime("%d/%m/%Y")
            corpo = f"Prezado(a) {nome_cliente},\n\n"
            if eh_reenvio:
                corpo += f"Seu pedido #{numero_pedido} teve informações atualizadas.\n\n• Nova versão do pedido em anexo\n• Versão: {versao_pdf}\n• Atualizado em: {data_atual}\n\nEsta versão substitui a anterior."
            else:
                corpo += f"Seu pedido #{numero_pedido} foi finalizado com sucesso!\n\n• Pedido em anexo\n• Data da venda: {data_atual}\n• Status: Concluído"
            corpo += f"\n\nObrigado pela sua compra!\n\nAtenciosamente,\n{self.config['EMAIL']['remetente_nome']}"
            msg.attach(MIMEText(corpo.strip(), 'plain', 'utf-8'))

            # Anexar PDF
            with open(caminho_pdf, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            nome_arquivo = f"Pedido_{numero_pedido}_v{versao_pdf}.pdf" if eh_reenvio else f"Pedido_{numero_pedido}.pdf"
            part.add_header('Content-Disposition', f'attachment; filename= {nome_arquivo}')
            msg.attach(part)

            # Enviar para todos os destinatários
            todos_destinatarios = [destinatario_principal] + lista_copia

            server = smtplib.SMTP(self.config['EMAIL']['smtp_servidor'], int(self.config['EMAIL']['smtp_porta']))
            server.starttls()
            server.login(self.config['EMAIL']['usuario'], self.config['EMAIL']['senha_app'])
            server.sendmail(self.config['EMAIL']['usuario'], todos_destinatarios, msg.as_string())
            server.quit()

            self.logger.info(f"{'REENVIO' if eh_reenvio else 'EMAIL'} enviado com sucesso - Pedido {numero_pedido} - Total de destinatários: {len(todos_destinatarios)}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao enviar email - Pedido {numero_pedido}: {e}")
            return False
            
    def processar_pedido(self, pedido):
        """Processa um pedido individual"""
        id_controle, numero_pedido = pedido['id'], pedido['numero']
        self.logger.info(f"Processando pedido {numero_pedido}...")
        self.atualizar_status_pedido(id_controle, 'StatusProcessamento', 'PROCESSANDO')
        
        try:
            if not self.validacao_geral(pedido): return False

            eh_reenvio = (pedido['motivo_processamento'] == "REENVIO_VERSAO_ATUALIZADA")
            enviar_para_cliente = pedido.get('enviar_email_cliente', 1) == 1  # Converte para boolean

            if self.enviar_email(
                pedido['email_cliente'],
                pedido['nome_cliente'],
                numero_pedido,
                pedido['caminho_pdf'],
                pedido['emails_copia'],
                eh_reenvio,
                pedido['versao_disponivel'],
                enviar_para_cliente
            ):
                query = "UPDATE ControleEmailPedidos SET StatusProcessamento = 'ENVIADO', EmailEnviado = 1, VersaoPdfEnviada = ?, DataEnvio = GETDATE(), UltimoErro = NULL, TentativasEnvio = 0 WHERE Id = ?"
                cursor = self.conexao_db.cursor()
                cursor.execute(query, (pedido['versao_disponivel'], id_controle))
                self.conexao_db.commit()
                self.logger.info(f"SUCESSO ao processar pedido {numero_pedido}")
                return True
            else:
                self.atualizar_status_pedido(id_controle, 'StatusProcessamento', 'PENDENTE', 'Erro no envio do email')
                return False
        except Exception as e:
            self.logger.error(f"Erro ao processar pedido {numero_pedido}: {e}")
            self.atualizar_status_pedido(id_controle, 'StatusProcessamento', 'PENDENTE', str(e))
            return False

    def validacao_geral(self, pedido):
        """Agrupa todas as validações de um pedido"""
        numero_pedido = pedido['numero']
        enviar_para_cliente = pedido.get('enviar_email_cliente', 1) == 1

        # Se deve enviar para cliente, valida se tem email do cliente
        if enviar_para_cliente and not pedido['email_cliente']:
            self.logger.warning(f"Pedido {numero_pedido}: EnviarEmailCliente=1 mas cliente sem email cadastrado.")
            self.atualizar_status_pedido(pedido['id'], 'StatusProcessamento', 'ERRO_VALIDACAO', 'Cliente sem email')
            return False

        # Se NÃO deve enviar para cliente, valida se tem emails de cópia
        if not enviar_para_cliente and not pedido['emails_copia']:
            self.logger.warning(f"Pedido {numero_pedido}: EnviarEmailCliente=0 mas não há EmailsCopia definidos.")
            self.atualizar_status_pedido(pedido['id'], 'StatusProcessamento', 'ERRO_VALIDACAO', 'EnviarEmailCliente=0 sem EmailsCopia')
            return False

        return True

    def executar_ciclo(self):
        """Executa um ciclo completo de processamento"""
        self.logger.info("=== Iniciando ciclo de processamento ===")
        if not self.conectar_banco(): return
        
        try:
            pedidos = self.buscar_pedidos_para_processar()
            for pedido in pedidos:
                self.processar_pedido(pedido)
        finally:
            if self.conexao_db: self.conexao_db.close()
        self.logger.info("=== Ciclo de processamento concluído ===")

    def testar_deteccao_versoes(self):
        """Função de teste para verificar detecção de versões de PDF sem enviar emails"""
        self.logger.info("=== TESTE: Verificando detecção de versões e sistema de tentativas ===")

        # Listar drivers ODBC disponíveis
        self.logger.info("=== Verificando drivers ODBC instalados ===")
        self.listar_drivers_odbc_disponiveis()

        if not self.conectar_banco():
            self.logger.error("Erro ao conectar ao banco para teste")
            return
        try:
            pedidos = self.buscar_pedidos_para_processar()
            for pedido in pedidos:
                self.logger.info(f"Pedido {pedido['numero']}: Motivo: {pedido['motivo_processamento']}")
        finally:
            if self.conexao_db: self.conexao_db.close()

class ExcelLogger:
    """Classe para gerenciar logs em formato Excel"""
    def __init__(self):
        self.caminho_base = r"C:\Users\Public\Documents\SRPP\scripts"
        os.makedirs(self.caminho_base, exist_ok=True)
        self.arquivo_atual = os.path.join(self.caminho_base, f"log_emails_{datetime.now().strftime('%Y-%m-%d')}.xlsx")

        try:
            if os.path.exists(self.arquivo_atual):
                self.workbook = openpyxl.load_workbook(self.arquivo_atual)
            else:
                self._criar_novo_workbook()
        except Exception as e:
            # Se arquivo estiver corrompido, renomeia e cria novo
            if os.path.exists(self.arquivo_atual):
                backup_name = self.arquivo_atual.replace('.xlsx', f'_corrupted_{datetime.now().strftime("%H%M%S")}.xlsx')
                os.rename(self.arquivo_atual, backup_name)
            self._criar_novo_workbook()

        self.aba_resumo = self.workbook["RESUMO"]
        self.aba_geral = self.workbook["LOG_GERAL"]

    def _criar_novo_workbook(self):
        """Cria um novo workbook Excel"""
        self.workbook = openpyxl.Workbook()
        self.workbook.remove(self.workbook.active)
        self.workbook.create_sheet("RESUMO")
        self.configurar_aba(self.workbook["RESUMO"], ["Data/Hora", "Pedido", "Cliente", "Email", "Status", "Motivo", "Tentativas", "Versão PDF", "Observações"])
        self.workbook.create_sheet("LOG_GERAL")
        self.configurar_aba(self.workbook["LOG_GERAL"], ["Timestamp", "Pedido", "Cliente", "Fase", "Detalhes", "Validações", "Erro", "Duração", "Thread"])
        self.salvar()

    def configurar_aba(self, aba, cabecalhos):
        """Configura cabeçalhos e formatação de uma aba"""
        aba.append(cabecalhos)
        for cell in aba[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        aba.freeze_panes = "A2"

    def log_resumo(self, **kwargs):
        """Adiciona entrada na aba RESUMO"""
        linha = [datetime.now().strftime("%d/%m/%Y %H:%M:%S")] + list(kwargs.values())
        self.aba_resumo.append(linha)
        self.salvar()

    def log_geral(self, **kwargs):
        """Adiciona entrada na aba LOG_GERAL"""
        linha = [datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]] + list(kwargs.values())
        self.aba_geral.append(linha)
        self.salvar()

    def salvar(self):
        """Salva o arquivo Excel"""
        try:
            self.workbook.save(self.arquivo_atual)
        except PermissionError:
            self.logger.warning("Não foi possível salvar o log do Excel, talvez esteja aberto.")

class PDFEventHandler(FileSystemEventHandler):
    """Handler para monitorar eventos de arquivos PDF"""
    def __init__(self, sistema_emails):
        self.sistema_emails = sistema_emails
        self.aguardar_segundos = int(sistema_emails.config.get('SISTEMA', 'aguardar_segundos_apos_arquivo', fallback=5))
        self.logger = sistema_emails.logger
        
    def on_created(self, event):
        """Chamado quando um arquivo é criado"""
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            self.logger.info(f"Novo PDF detectado: {os.path.basename(event.src_path)}")
            time.sleep(self.aguardar_segundos)
            self.sistema_emails.executar_ciclo()
            
    def on_modified(self, event):
        """Chamado quando um arquivo é modificado"""
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            self.logger.info(f"PDF modificado detectado: {os.path.basename(event.src_path)}")
            time.sleep(self.aguardar_segundos)
            self.sistema_emails.executar_ciclo()

def main():
    """Função principal"""
    def signal_handler(sig, frame):
        print('\nEncerrando sistema...')
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        sistema = SistemaEnvioEmails()
        if len(sys.argv) > 1 and sys.argv[1] == "--teste":
            print("MODO TESTE: Verificando detecção de versões (SEM ENVIAR EMAILS)")
            sistema.testar_deteccao_versoes()
            return

        print("Sistema de Envio de Emails iniciado!")
        caminho_pdfs = sistema.config['PDFS']['caminho']
        print(f"Monitorando pasta: {caminho_pdfs}")
        
        if sistema.config.getboolean('SISTEMA', 'verificacao_inicial'):
            print("Executando verificação inicial...")
            sistema.executar_ciclo()

        event_handler = PDFEventHandler(sistema)
        observer = Observer()
        observer.schedule(event_handler, caminho_pdfs, recursive=False)
        observer.start()
        
        print("Pressione Ctrl+C para encerrar.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        print("Sistema encerrado.")
    except Exception as e:
        print(f"Erro fatal ao inicializar: {e}")

if __name__ == "__main__":
    main()