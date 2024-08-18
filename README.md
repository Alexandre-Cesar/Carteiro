# Carteiro
Este é um projeto de envio de e-mails usando python. Ele utiliza as bibliotecas `smtp` e `email` para escrita e incorporação do e-mail.

## Como usar

### Instaciar objeto 
Para começar, importe a classe `Carta` para o seu código python, instacie-a com o as informações de remetente, destinatario, senha, host e porta, certifique-se que as informações estão corretas paraobter o envio do e-mail. Para a senha é necessário a criação de umasenha de app, mais informações no link abaixo:  
https://support.google.com/accounts/answer/185833?hl=pt-BR


```python
from carteiro import carta

mensageiro = carteiro.carta(sender, receiver, subject, password, host, port)
``` 
### Funções  

#### Escrever e-mail  
Para a escrita de um e-mail existem duas funções:  
`escrever_mensagem` adiciona informações de assunto e corpo do e-mail.

```python
mensagem =  mensageiro.escrever_mensagem('assunto da mensagem','olá, e-mail enviado utilizando a função de escrita de mensagem') 
``` 

`escrever_email_anexado` adiciona informações de assunto e corpo do e-mail junto a arquivos para anexar. A função também permite que utilizar um arquivo hmtl para criação do corpo do arquivo.

```python
html_file = 'mensage_footbal.html'
anexos ={
    '2022-2023_footbal_players_status.csv': 'csv',
    '2022-2023_footbal_players_status.txt': 'docx'
}
mensageiro = carteiro.carta(sender, receiver, subject, password, host, port)
mensagem =  mensageiro.escrever_email_anexado('assunto da mensagem',html_file, True, anexos)
```   

#### Escrever e-mail 
Após a composição do e-mail, enviar utilizando a função `enviar_email`, após criação da mensagem:

```python

mensagem = mensageiro.escrever_mensagem('envio de mensagem','olá, Deu certo a função de escrita de mensagem')

mensageiro.enviar_email(mensagem)
``` 

## Exemplo

```python
from carteiro import carta

mensageiro = carteiro.carta(sender, receiver, subject, password, host, port)

mensagem = mensageiro.escrever_mensagem('envio de mensagem','olá, Deu certo a função de escrita de mensagem')

mensageiro.enviar_email(mensagem)
```
mais exemplos no notebook executer.ipynb








