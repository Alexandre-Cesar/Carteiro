import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import subprocess
import base64

import imaplib
import email
from email.policy import default

class Carta():
    
    def __init__(self, email_configs: dict):
        self.sender = email_configs["sender"]
        self.receiver = email_configs["receiver"]
        self.password = email_configs["password"]
        self.host = email_configs["host"]
        self.port = email_configs["port"]

    def __set_mensagem(self):
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.receiver

        return message

    #Envio de arquivos
    def escrever_mensagem(self, assunto:str, texto:str):
        '''
        Envia mensagem sem utilizar html, apenas usando um string
        '''

        message = self.__set_mensagem()
        message['Subject'] = assunto
        message.attach(MIMEText(texto, 'plain'))   

        return message

    

    def __adiciona_anexo(self, file, file_tipe):
        '''
        file: path do arquivo
        file_tipe: tipo do arquivo 

        Cria anexo de mensagem realizando a leitura do arquivo dentro do diretório e indicando o tipo de arquivo que será escrito dentro do e-mail 
        '''
        

        splited = file.split('/')[-1]
        filename = splited.split('.')[:-1]
        filename = ".".join(filename)

        command = f"hdfs dfs -cat {file}"
        output = subprocess.check_output(command, shell=True)
        attachment = output.decode('utf-8')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}.{file_tipe}")
        return part


    def escrever_email_anexado(self, assunto:str, corpo:str, ishtml:bool,  anexos:dict):
        ''''
        precisa de:
          Assunto e corpo ser string
          indicar  ishtml ser True or False
          um dicionario com as informações de caminho de arquivo e o tipo que queira ser enviado
        '''
        
        #corpo do e-mail
        message = self.__set_mensagem()
        message['Subject'] = assunto


        #texto do e-mail
        if ishtml:
            body = open(corpo, 'r').read()

            message.attach(MIMEText(body, 'html'))
        else:
            body = corpo
            message.attach(MIMEText(body, 'plain'))

        # Anexo do arquivo 
        for a in anexos:
            
            part = self.__adiciona_anexo(a, anexos[a])
            message.attach(part)
        
        return message

    
    def enviar_email(self, message):
        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.sender, self.password)
            text = message.as_string()
            smtp.sendmail(self.sender, self.receiver, text)   
        print(f'enviado para {self.receiver}')


    #extração de arquivos
    def __write_file_in_hdfs(content, hdfs_path):
        '''
        pode ser usado em outros projetos!
        cria um arquivo em branco no formato do arquivo a ser escrito e depois adiciona o conteudo nele
        resolvendo problemas na hora de escrever arquivos como pdf por exemplo
        '''

        try:
            # Usamos subprocess.Popen para enviar o buffer via stdin
            with subprocess.Popen(['hadoop', 'fs', '-put', '-', hdfs_path], stdin=subprocess.PIPE) as proc:
                # Escreve o buffer diretamente para o stdin do comando hadoop fs -put
                proc.communicate(input=content)
            
            print(f"Arquivo salvo com sucesso no HDFS em: {hdfs_path}")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao gravar o arquivo no HDFS: {e}")

    def guardar_anexos(self, hdfs_path):
        '''
        feito para realizar a extração de arquivos em anexo para dentro do hdfs
        hdfs_path: caminho para o  arquivo ser escrito dentro do hdfs ex. "/data_lake/landing/pasta/"
        '''

        # Conectar à caixa de e-mail
        mail = imaplib.IMAP4_SSL(self.host)
        mail.login(self.receiver, self.password)
        mail.select('contas_consumo')
        # Busca por e-mails não lidos ou com anexos (use filtros conforme necessário)
        #status, email_ids = mail.search(None, '(FROM "Alexandre Cesar Dias Goncalves")')
        status, email_ids = mail.search(None, 'UNSEEN')
        print(f'e-mails encontrados:{status}')
        email_ids = email_ids[0].split()
        # Loop para cada e-mail
        for e_id in email_ids:
            status, email_data = mail.fetch(e_id, '(RFC822)')
            raw_email = email_data[0][1]
            msg = email.message_from_bytes(raw_email, policy=default)
            # Extrair anexos
            for part in msg.iter_attachments():
                filename = part.get_filename()
                if filename:
                    hdfs_path = f"{hdfs_path}{filename}"
                    content = part.get_payload(decode=True)
                    self.__write_file_in_hdfs(content, hdfs_path)

        mail.logout()
