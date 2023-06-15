import tkinter as tk
from tkinter import filedialog
import paramiko
import configparser

config = configparser.ConfigParser()
config.read('config.ini')  # Lê o arquivo de configuração existente (se existir)

def fazer_login():
    servidor = campo_servidor.get()
    usuario = campo_usuario.get()
    senha = campo_senha.get()
    destino = campo_destino.get()

    hostname = servidor
    username = usuario
    password = senha
    remote_path = destino
    


    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, username=username, password=password)
        
        resultado.set("Conexão bem-sucedida!")
        
    except paramiko.AuthenticationException:
        resultado.set("Falha na autenticação SSH")
        
    except paramiko.SSHException as ssh_err:
        resultado.set("Erro SSH: " + str(ssh_err))
        
    finally:
        client.close()
    config['UltimosDados'] = {
        'Servidor': servidor,
        'Usuario': usuario,
        'Senha': senha,
        'destino': destino
    }
    
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
        
def fazer_upload():
    arquivo = filedialog.askopenfilename()
    
    servidor = campo_servidor.get()
    usuario = campo_usuario.get()
    senha = campo_senha.get()
    destino = campo_destino.get()
    
    hostname = servidor
    username = usuario
    password = senha
    remote_path = destino
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, username=username, password=password)
        
        sftp = client.open_sftp()
        
        sftp.put(arquivo, remote_path)
        
        sftp.close()
        
        resultado.set("Upload concluído com sucesso!")
        
    except paramiko.AuthenticationException as e:
        resultado.set(f"Falha na autenticação SSH: {e}")
        
    except paramiko.SSHException as ssh_err:
        resultado.set("Erro SSH: " + str(ssh_err))
        
    finally:
        client.close()

    config['UltimosDados'] = {
        'Servidor': servidor,
        'Usuario': usuario,
        'Senha': senha,
        'destino':destino
    }
    
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

janela = tk.Tk()
janela.title("Upload via SSH")


label_servidor = tk.Label(janela, text="Endereço do servidor:")
label_servidor.pack()
campo_servidor = tk.Entry(janela)
campo_servidor.pack()

label_usuario = tk.Label(janela, text="Usuário:")
label_usuario.pack()
campo_usuario = tk.Entry(janela)
campo_usuario.pack()

label_senha = tk.Label(janela, text="Senha:")
label_senha.pack()
campo_senha = tk.Entry(janela, show="*")
campo_senha.pack()

botao_login = tk.Button(janela, text="Login no servidor", command=fazer_login)
botao_login.pack()

label_destino = tk.Label(janela, text="Caminho de destino no servidor:")
label_destino.pack()
campo_destino = tk.Entry(janela)
campo_destino.pack()



botao_upload = tk.Button(janela, text="Selecionar arquivo e enviar", command=fazer_upload)
botao_upload.pack()

resultado = tk.StringVar()
label_resultado = tk.Label(janela, textvariable=resultado)
label_resultado.pack()


if 'UltimosDados' in config:
    campo_servidor.insert(tk.END, config['UltimosDados'].get('Servidor', ''))
    campo_usuario.insert(tk.END, config['UltimosDados'].get('Usuario', ''))
    campo_senha.insert(tk.END, config['UltimosDados'].get('Senha', ''))
    campo_destino.insert(tk.END, config['UltimosDados'].get('destino',''))


janela.mainloop()
