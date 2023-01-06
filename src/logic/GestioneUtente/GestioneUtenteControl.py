import hashlib
from src.logic.model.Utente import Utente

from src.logic.model.UtenteDAO import UtenteDAO
from src.logic.model.LicenzaDAO import LicenzaDAO
from src.logic.model.Licenza import Licenza
from src.logic.model.MetodoDiPagamentoDAO import MetodoDiPagamentoDAO
from src.logic.model.MetodoDiPagamento import MetodoDiPagamento
from datetime import timedelta
from datetime import datetime

from flask import jsonify, request, render_template
from src import app
from flask_login import current_user, login_user
from flask import url_for


class UtenteControl():
    @app.route("/login", methods = ["GET", "POST"])
    def login():
        """
        Reads the users credentials from a https request if they match with one entry
        on the database, the system change his state from anonymous to logged user
        :return: redirect to index page
        """
        if request.method == "POST" :
            successo = False
            email = request.form.get("email")
            password = request.form.get("password")
            hashed_password = hashlib.sha512(password.encode()).hexdigest()
            login_attempt : Utente = UtenteDAO.trovaUtenteByEmail(email)

            if not login_attempt:
                print("Utente non registrato")
                successo = False
            
            if login_attempt.password == hashed_password:
                login_user(login_attempt, duration=timedelta(days=365), force=True)
                successo = True
                
            else:
                print("password errata")
                successo = False

            if successo:
                return "email utente loggato: " + current_user.email
            else:
                return render_template("login.html")        
        else:
            return render_template("login.html")

    @app.route("/register", methods = ["GET", "POST"])
    def registrazioneConCodiceDiAccesso():
        if request.method == "POST": 
            richiesta = request.form
            email = richiesta.get("email")
            nome = richiesta.get("nome")
            cognome = richiesta.get("cognome")
            password = hashlib.sha512(richiesta.get("password").encode()).hexdigest()
            dataDiNascita = datetime.strptime(richiesta.get("dataNascita"), "%Y-%m-%d")
            codiceDiAccesso = richiesta.get("codice")
            #TODO: Implementare la verifica dell'indirizzo
            indirizzo = richiesta.get("indirizzo")
            slotUtente = UtenteDAO.trovaUtenteByCodiceDiAccesso(codiceDiAccesso)
            risposta = {
                "emailUsata": False,
                "codiceNonValido": False,
                "utenteRegistrato" : False
            }

            #Se l'email è già usata il server avviserà il front-end
            if UtenteDAO.trovaUtenteByEmail(email) != None:
                risposta["emailUsata"] = True
            #Se il codice è già usato oppure non è valido il server avviserà il front end
            elif slotUtente == None or slotUtente.nome != None:
                risposta["codiceNonValido"] = True
            #Altrimenti si recupera lo slot Utente dal database lo si modifica con i dati utente
            else:
                slotUtente.nome = nome
                slotUtente.cognome = cognome
                slotUtente.password = password
                slotUtente.email = email
                slotUtente.dataNascita = dataDiNascita
                slotUtente.indirizzo = indirizzo
                UtenteDAO.modificaUtente(slotUtente)
                risposta["utenteRegistrato"] = True 
                
            return jsonify(risposta)
        else:
            return render_template("register.html")
            
    @app.route("/registerf")
    def registrazioneFarmer():
        richiesta = request.args
        email = richiesta.get("email")
        nome = richiesta.get("nome")
        cognome = richiesta.get("cognome")
        password = hashlib.sha512(richiesta.get("password").encode()).hexdigest()
        dataDiNascita = datetime.strptime(richiesta.get("dataNascita"), "%Y-%m-%d")
        partitaiva = richiesta.get("partitaiva")
        licenza = richiesta.get("licenza")
        numerocarta = richiesta.get("numerocarta")
        titolare = richiesta.get("titolare")
        scadenza = richiesta.get("scadenza")
        cvv = richiesta.get("cvv") 
        #TODO: Implementare la verifica dell'indirizzo
        indirizzo = richiesta.get("indirizzo")
        risposta = {
            "emailUsata": False,
            "codiceNonValido": False,
            "utenteRegistrato" : False
        }

        #Se l'email è già usata il server avviserà il front-end
        if UtenteDAO.trovaUtenteByEmail(email) != None:
            risposta["emailUsata"] = True
        else:
            utente = Utente("", nome, cognome, email, password, "farmer", dataDiNascita, partitaiva, None, indirizzo)
            id = UtenteDAO.creaUtente(utente)
            #TODO decidere i parametri delle licenze
            l = Licenza("", licenza, 5000, datetime.now(), datetime.now(), False, id)
            LicenzaDAO.creaLicenza(l)
            m = MetodoDiPagamento("", numerocarta, titolare, scadenza, cvv, id)
            MetodoDiPagamentoDAO.creaMetodo(m)

            risposta["utenteRegistrato"] = True 
        #Invio della risposta al server in formato json
        return jsonify(risposta)

        
        

        

        
        

