import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class Carta():
    
    def __init__(self, sender:str, receiver, password:str, host, port:int):
        self.sender = sender
        self.receiver = receiver
        self.password = password
        self.host = host
        self.port = port

    def set_mensagem(self):
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.receiver

        return message

    def escrever_mensagem(self, assunto:str, texto:str):
        '''
        Envia mensagem sem utilizar html, apenas usando um string
        '''

        message = self.set_mensagem()
        message['Subject'] = assunto
        message.attach(MIMEText(texto, 'plain'))   

        return message

    

    def adiciona_anexo(self, file, file_tipe):
        '''
        file: path do arquivo
        file_tipe: tipo do arquivo 

        Cria anexo de mensagem realizando a leitura do arquivo dentro do diretório e indicando o tipo de arquivo que será escrito dentro do e-mail 
        '''
        splited = file.split('/')[-1]
        filename = splited.split('.')[0]
        attachment = open(file, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
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
        message = self.set_mensagem()
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
            
            part = self.adiciona_anexo(a, anexos[a])
            message.attach(part)
        
        return message

    
    def enviar_email(self, message):
        with smtplib.SMTP_SSL(self.host, self.port) as smtp:
            smtp.login(self.sender, self.password)
            text = message.as_string()
            smtp.sendmail(self.sender, self.receiver, text)   
        print(f'enviado para {self.receiver}')
