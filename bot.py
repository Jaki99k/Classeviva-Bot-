import telepot
import telegram
import datetime
import calendar
from classeviva import Session

sn = Session()
loginOK = None
now = datetime.datetime.now()

def agenda(filtro):
    ''' Questa funzione la implementerò piu avanti 
    if filtro == 'all': #STAMPA COMPITI DA SEMPRE
        dateStart = datetime.date(2018, 9, 12)
        dateEnd = datetime.date(2019, 6, 9)
        print(sn.agenda(begin=dateStart, end=dateEnd))
    elif filtro == 'mese':
        print("Giorno attuale :", now.day)
        print("Inizio mese : ", now.day - now.day + 1)
        lastDay = calendar.monthrange(now.year, now.month)
        dateStart = datetime.date(now.year, now.month, now.day - now.day + 1)
        dateEnd = datetime.date(now.year, now.month, lastDay[1])
        print(sn.agenda(begin=dateStart, end=dateEnd))
    elif filtro == 'week': #STAMPA COMPITI DELLA SETTIMANA
        giornoSettimana = datetime.datetime.today().weekday() #4
        #print(int(now.day))
        #print(int(giornoSettimana))
        dateStart = datetime.date(now.year, now.month, int(now.day) - giornoSettimana)
        dateEnd = dateStart + datetime.timedelta(days=7)
        print(sn.agenda(begin=dateStart, end=dateEnd))
        #print(dateStart)
        #print(dateEnd) 
    elif filtro == 'day':
        giorno = datetime.date(now.year, now.month, now.day)
        print(sn.agenda(begin=giorno, end=giorno))
        '''

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        global alunno
        global loginOK
        conta = 0
        itt = 0
        totale = "<b>Elenco Materie e insegnanti : </b>"
        lessons = "<b> Le lezioni di oggi sono le seguenti </b>\n"
        #print("Messaggio di tipo testo!")
        messaggio = msg['text']
        print(messaggio)
        if messaggio[0:6] == '/login':
            alunno = {}
            username = messaggio[6:16]
            password = messaggio[17:25]
            print("Username : ", username)
            print("Password : ", password)
            print(sn.login(username=username, password=password))
            alunno = sn.login(username=username, password=password)
            #bot.sendMessage(chat_id, "Login effettuato con ID : " + str(alunno['id']))
            bot.sendMessage(chat_id, '<b>Login effettuato con successo!</b>', telegram.ParseMode.HTML)
            bot.sendMessage(chat_id, "Loggato come : " + str(alunno['first_name'] + ' ' + str(alunno['last_name'])))
            if bool(alunno) == True:
                loginOK = True
            else:
                loginOK = False
        if messaggio[0:8] == '/materie': #VISUALIZZA LE MATERIE E I CORRISPONDENTI INSEGNANTI
            if loginOK is not True:
               bot.sendMessage(chat_id, "<b>Non sei loggato!</b>\nPrima di poter accedere a questa funzione effettua il /login <i> username password </i>", telegram.ParseMode.HTML)
            else:
                materie = sn.subjects()
                materie = materie['subjects']
                #subjects = {}
                
                for x in materie:
                    insegnante = materie[conta]['teachers']
                    nomeMateria = materie[conta]['description']
                    print(str(conta) + ')' + str(nomeMateria.split('-')[0])) #LA FUNZIONE SPLIT DIVIDE LA SRTINGA NEL MOMENTO IN CUI INCONTRA IL CATATTERE INDICATO
                    #INOLTRE SUCCESSIVAMENTE INDICO DI PRENDERE L'ELEMENTO 0 DALLA LISTA CHE CONTIENE IL NOME DELLA MATERIE IN ITALIANO
                    totale += '<b>' + str(conta) + '</b>' + ')' + nomeMateria.split('-')[0] + ' 📖' + '\n\n'
                    itt = 0
                    for i in insegnante:
                        nomeInsegnante = insegnante[itt]['teacherName']
                        totale += '<i>' + nomeInsegnante + '</i>' + ' 👨‍🏫' + '\n\n'
                        print("Insegnante : " + str(nomeInsegnante))
                        itt += 1
                    conta += 1

                bot.sendMessage(chat_id, totale, telegram.ParseMode.HTML)
                
                
        if messaggio[0:7] == '/agenda': #VISUALIZZA TUTTI I COMPITI IN AGENDA
            #DOPO AD AGENDA INSERIRE PERIODO (ALL, WEEK, DAY)
            #print("I messaggi in agenda sono i seguenti")
            #filtro = input("Inserisci filtro\nFiltro : ")
            '''Da terminare in attesa che vengano inseriti dei compiti'''
            if loginOK is not True:
                bot.sendMessage(chat_id, "<b>Non sei loggato!</b>\nPrima di poter accedere a questa funzione effettua il /login <i> username password </i>", telegram.ParseMode.HTML)
            else:
                oggi = datetime.date(now.year, now.month, now.day)
                print(sn.agenda(begin=oggi, end=oggi))

        if messaggio[0:8] == '/lezioni':
            conta = 0
            if loginOK is not True:
                bot.sendMessage(chat_id, "<b>Non sei loggato!</b>\nPrima di poter accedere a questa funzione effettua il /login <i> username password </i>", telegram.ParseMode.HTML)
            else:
                lezioni = sn.lessons()
                lezioni = lezioni['lessons']
                for x in lezioni:
                    if lezioni[conta]['subjectDesc'] != 'SOSTEGNO':
                        lessons += 'Modulo numero : ' + '<b>' + str(lezioni[conta]['evtHPos']) + '</b>' + '\n\n'
                        lessons += '<i>' + 'Materie lezione : ' + str(lezioni[conta]['subjectDesc']).split('-')[0] + '</i>' + '\n'
                        lessons += 'Insegnante : ' + '<i>' + str(lezioni[conta]['authorName']) + '</i>' + '\n'
                        lessons += 'Tipo lezione : ' + str(lezioni[conta]['lessonType']) + '\n\n'
                    conta += 1
                
                bot.sendMessage(chat_id, lessons, telegram.ParseMode.HTML)

                #print(lessons)


            
TOKEN = "607128868:AAFYbAun6dmow7sQd0ChIOCC93VTzcNPjMM"
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message})

import time
while 1:
    time.sleep(10)
