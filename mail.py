import smtplib, ssl
import covidStats as cS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():
    
    #COUNTRIES
    countries = [cS.country('CH'), cS.country('ES'), cS.country('IT'), cS.country('FR'), cS.country('US'), cS.country('CN'), cS.country('GB'), cS.country('EG')]
    
    
    #change to ur language
    headers =['Pais', 'Casos', '-por 100k', 'Muertes', 'Recoveries', '+casos 14 dias', '-por 100k'] 

    text = ''
    html = ''

    headerOnly = '' # for making html
    for h in headers:
        headerOnly += addZeros(h)
        text+= addZeros(h)
    headerOnly+='\n'
    text+='\n'


    listPerCountry = []
    for i in countries:
        l = i.getData()
        countryText = ''
        for item in l:
            if type(item) == int:
                countryText += addZeros(item)
            else:
                countryText += addZeros(item)
        listPerCountry.append(countryText)
        countryText+='\n'
        text+=countryText
    html = makeHtml(headerOnly, listPerCountry)

    html = '<pre><h2>Hola aqui tiene las estadisticas:</h2><h3>Que disfrutes</h3><br>' + html + '</pre>'

    #print(text)
    #print(html)
    
    
    #text = text.encode('utf-8')
    
    port = 465  # For SSL
    password = input("Type your password and press enter: ")
    
    #List of emails
    rEmails = ['', '']
    #if only 1 email change to string or take [0] when rEmails is referenced

    sender_email = ''
    
    message = MIMEMultipart("alternative")
    message["subject"] = "Informe Covid Semanal"
    message["From"] = sender_email
    message["To"] = ", ".join(rEmails) #change if only 1 email
    
    p1 = MIMEText(text, "plain") #if email doesnt support html
    p2 = MIMEText(html, 'html')
    
    message.attach(p1)
    message.attach(p2)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, rEmails, message.as_string())


#construct html message
def makeHtml(textOnlyHeader, messageList):
    html = ''
    html = '<p style="margin:0;"><b>' + textOnlyHeader + '</b></p><hr>'
    for j in range(0, len(messageList)):
        if j%2 == 0:
            col = 'grey'
        else:
            col = 'black'
        html+= '<p style="margin:0; color:'+ col + ';">' + str(messageList[j]) + '</p>'
    return html


#to make a string 'table': each element contains same nb of spaces
def addZeros(string):
    spaces = '                '
    if type(string) == int:
        string = "{:,}".format(string)
    i = len(spaces) - len(string)
    result = str(string) + spaces[0:i]
    return result

if __name__ == "__main__":
    main()
