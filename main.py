import streamlit as st
import paramiko
from datetime import datetime
import logging
import socket
import time
import threading

st.set_page_config(page_title='Painel PDV')
# Habilitar logs de debug do Paramiko
logging.basicConfig(level=logging.DEBUG)

# Função para gerar a senha com base no número do PDV, dia e mês atuais
def calculate_password(pdv_number, is_root):
    if is_root:
        return "1"  # Senha fixa para root, ajuste conforme necessário
    today = datetime.now()
    day_month = int(f"{today.day}{today.month}")
    password_number = day_month + int(pdv_number)
    password = f"pdv@{password_number}"
    return password

# Função para obter o IP fixo
def get_fixed_ip(pdv_number):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS, mas não envia nenhum dado
        ip_address = s.getsockname()[0]  # Obtém o IP usado nessa conexão
    finally:
        s.close()

    if not ip_address:
        raise Exception("Não foi possível obter o IP do computador.")

    corte = ip_address.split('.')
    faixa = corte[2]
    return f'172.23.{faixa}.1{pdv_number}'

# Função para reiniciar a aplicação em um PDV específico
def reiniciar_pdv(pdv_num, comando, is_root):
    # Configuração do host do PDV e geração da senha
    try:
        host = get_fixed_ip(pdv_num)  # Obtém o IP fixo
    except Exception as e:
        st.error(f"Erro ao obter IP fixo: {e}")
        return

    usuario = "root" if is_root else "suporte"
    senha = calculate_password(pdv_num, is_root)

    st.write(f"Conectando ao {host} com o usuário {usuario}.")

    # Criação do cliente SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Conectar ao PDV via SSH com timeout
        ssh.connect(hostname=host, username=usuario, password=senha, timeout=10)
        st.write(f"Conectado com sucesso ao {host}")

        # Executar o comando escolhido
        stdin, stdout, stderr = ssh.exec_command(comando)

        # Aguardar até que o comando seja concluído
        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            st.write(f"Comando executado com sucesso no PDV {pdv_num}. Aguardando aplicação voltar...")
        else:
            st.write(f"Erro ao executar comando no PDV {pdv_num}. Código de saída: {exit_status}")

        # Aguardar um tempo para garantir que a aplicação suba corretamente (pode ajustar o tempo conforme necessário)
        time.sleep(10)

        st.write(f"A aplicação no PDV {pdv_num} deve estar operacional agora.")

    except paramiko.AuthenticationException as e:
        st.error(f"Falha de autenticação no PDV {pdv_num}: {e}")
    except paramiko.SSHException as e:
        st.error(f"Erro de conexão SSH no PDV {pdv_num}: {e}")
    except Exception as e:
        st.error(f"Erro ao conectar no PDV {pdv_num}: {e}")

    finally:
        # Fechar a conexão SSH, se não estiver fechada
        if ssh.get_transport() and ssh.get_transport().is_active():
            ssh.close()
        st.write(f"Conexão com o PDV {pdv_num} encerrada.")

# Função principal do Streamlit
def start_interface():
    st.title("Painel PDV")

    pdv_num = st.text_input("Número do PDV", max_chars=2)
    is_root = st.checkbox("Conectar como root")

    comandos = {
        "Reiniciar PDV": "reboot",
        "Reiniciar Aplicação": "ps-restart-application.sh",
        "Ajustar Resolução": '''xrandr --newmode "1920x1080_60.00" 173.00 1920 2048 2248 2576 1080 1083 1088 1120 -hsync +vsync; xrandr --addmode VGA-1 "1920x1080_60.00"; xrandr --output VGA-1 --mode "1920x1080_60.00"; ps-restart-application.sh'''
    } if is_root else {
        "Reiniciar PDV": "sudo init 6",
        "Reiniciar Aplicação": "sudo restart-application.sh",
        "Ajustar Resolução": '''xrandr --newmode "1920x1080_60.00" 173.00 1920 2048 2248 2576 1080 1083 1088 1120 -hsync +vsync; xrandr --addmode VGA-1 "1920x1080_60.00"; xrandr --output VGA-1 --mode "1920x1080_60.00"; sudo restart-application.sh''',
        "Atualizar PDV": "sudo update-pdv-app"
    }

    comando = st.selectbox("Escolha um comando", options=list(comandos.keys()))
    
    if st.button("Executar comando"):
        if pdv_num:
            reiniciar_pdv(pdv_num.zfill(2), comandos[comando], is_root)
        else:
            st.error("Por favor, insira o número do PDV.")

if __name__ == "__main__":
    start_interface()
