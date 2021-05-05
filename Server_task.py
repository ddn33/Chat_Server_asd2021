#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 17:59:08 2021

@author: francescaronci
"""
import flask
from flask import request, jsonify
import random
from datetime import datetime
import time
import secrets

def update_lista_utenti(utenti_registrati):
    result = {utenti_registrati[i]['username']:utenti_registrati[i]['password'] for i in range(len(utenti_registrati))}
    return result

def token_scaduto(user):
    for tk in token:
        if tk['username'] == user:
            user_token = tk
            break
    if time.time() - user_token['data'] > 1800:
        return True
    else:
        return False
    
def missing_token(user):
    for tk in token:
        if tk['username'] == user:
            return False   
    return True
    
            
        
    


app = flask.Flask(__name__)

messaggi = [
    {
    'mittente': 'Marco',
    #'token': random.getrandbits(128),
    'destinatario': 'Laura',
    'messaggio': 'ciao',
    'messaggio_consegnato': True
    },
    {
    'mittente': 'Paolo',
    #'token': random.getrandbits(128),
    'destinatario': 'Franca',
    'messaggio': 'come stai',
    'messaggio_consegnato': True

    }
    ]

utenti_registrati= [
        {
            'username':'Marco',
            'password': 1234
            }
        ]

token = [
    {
        'username':'Marco',
        'token': '....',
        'data': '....'
        
        #utente token data scadenza
    
    }
    ]

@app.route('/api/v1/resources/registrazione',methods=['POST'])
def Registration():
   nuovo_utente= {}

   lista_utenti = update_lista_utenti(utenti_registrati)

   if request.args['username'] not in lista_utenti:
        nuovo_utente['username']=request.args['username']
        nuovo_utente['password']=int(request.args['password'])
        #nuovo_utente['token']=str(random.getrandbits(128))
        nuovo_utente['token']=56643

        utenti_registrati.append(nuovo_utente)

        print('utente registrato correttamente')

        return jsonify(utenti_registrati)


   elif request.args['username'] in lista_utenti:

        print('nome utente già in uso')

        return ('''<h2> ERROR: nome utente già in uso</h2>''')

@app.route('/api/v1/resources/autenticazione',methods=['POST'])
def Authentication():
    
        lista_utenti = update_lista_utenti(utenti_registrati)
        
        if request.args['username'] in lista_utenti.keys():
            
            if int(request.args['password'])== lista_utenti[request.args['username']]:
                if token_scaduto(request.args['username']) or missing_token(request.args['username']):
                    for tk in token:
                        if tk['username'] == request.args['username']:
                            tk['username'] = request.args['username']
                            tk['token']= secrets.token_hex(16)
                            tk['data']= time.time()                                              
                            return ('''<h2>AUTENTICAZIONE RIUSCITA </h2>''')
                else:
                   pass               
            else:
                return ('''<h2> PASSWORD ERRATA </h2>''')

        else:

            ('''<h2>L'UTENTE NON E' REGISTRATO</h2>''')


@app.route('//api/v1/resources/invio', methods=['POST'])
def send():
    lista_utenti = update_lista_utenti(utenti_registrati)
    if request.args['destinatario'] not in lista_utenti.keys():
        return ''' <h1> Il Destinatario non esiste <h1>'''
    elif token_scaduto(request.args['username']):
        return ''' <h1>Sessione scaduta, effetuare autenticazione<h1> '''
    else :
        nuovo_messaggio = {}
        #salvataggio messaggio database messaggi
        nuovo_messaggio['mittente'] = request.args['username']
        nuovo_messaggio['destinatario'] = request.args['destinatario']
        nuovo_messaggio['messaggio'] = request.args['messaggio']
        nuovo_messaggio['messaggio'] = request.args['timestamp']
        nuovo_messaggio['messaggio_consegnato'] = False
        
        messaggi.append(nuovo_messaggio)
        return '''messaggio inviato con successo'''
    
    
# metodo che retituise a storia di tutti i messaggi rivevuti dal client
# @app.route('/api/v1/resources/messaggi/all', methods=['GET'])
# def mess_all():
#     return jsonify(messaggi)



@app.route('//api/v1/resources/Receive', methods=['GET'])
def receive():
    lista_utenti = update_lista_utenti(utenti_registrati)
    if token_scaduto(request.args['username']):
        return ''' <h1>Sessione scaduta, effetuare autenticazione</h1> '''
    else: #sessione valida
        
        messaggi_ricevuti = []
        for messaggio in messaggi:
            if request.args['username'] == messaggio['destinatario'] and messaggio['messaggio_consegnato'] == False:
                messaggi_ricevuti.append(messaggio)
                messaggio['messaggio_consegnato'] = True
        if messaggi_ricevuti == []:
            return ''' <h1> Non ci sono nuovi messaggi </h1>'''
        else:
            return messaggi_ricevuti
    
    

@app.route('/api/v1/resources/utenti_registrati/all', methods=['GET'])
def utenti_all():
    return jsonify(utenti_registrati)






