#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
            
            if time.time() - user_token['data'] > 1800:
                
                
                return True
        
            else:
                
                
                return False
    return False

def missing_token(user):
    for tk in token:
        if tk['username'] == user:
            return False
    return True

def token_errato(user,nuovo_token):
    for tk in token:
        if tk['username'] == user:
            if nuovo_token == tk['token']:
                return False
    return True
    
           
    


app = flask.Flask(__name__)

messaggi = [
            {
            'mittente': 'Marco',
            #'token': random.getrandbits(128),
            'destinatario': 'Laura',
            'messaggio': 'ciao',
            #'messaggio_consegnato': True
            },
            {
            'mittente': 'Paolo',
            #'token': random.getrandbits(128),
            'destinatario': 'Franca',
            'messaggio': 'come stai',
            #'messaggio_consegnato': True
            
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

@app.route('/api/v1/resources/registration',methods=['POST'])
def Registration():
        nuovo_utente = {}
   
        lista_utenti = update_lista_utenti(utenti_registrati)

        if request.args['username'] not in lista_utenti:
            nuovo_utente['username']=request.args['username']
            nuovo_utente['password']=int(request.args['password'])
            
            utenti_registrati.append(nuovo_utente)
            
            message = {'message': 'utente registrato correttamente'}
            #nuovo_utente['token']=str(random.getrandbits(128))
            #nuovo_utente['token']=56643
            
            # print('utente registrato correttamente')
            response = {**nuovo_utente,**message}
            return jsonify(response)
           
           
        elif request.args['username'] in lista_utenti:
            # print('nome utente già in uso')
            return ('''<h2> ERROR: nome utente già in uso</h2>''')

@app.route('/api/v1/resources/authentication',methods=['POST'])
def Authentication():
    
    lista_utenti = update_lista_utenti(utenti_registrati)
    
    if request.args['username'] in lista_utenti.keys():
        
        if int(request.args['password'])== lista_utenti[request.args['username']]:
            
                if token_scaduto(request.args['username']):
                    for tk in token:
                        if tk['username'] == request.args['username']:
                            # tk['username'] = request.args['username'] ridondante, è già assegnato il nome
                            tk['token']= secrets.token_hex(16)
                            tk['data']= time.time()
                            message = {'message': '''IL TOKEN SCADUTO E' STATO AGGIORNATO, AUTENTICAZIONE RIUSCITA'''}
                            response = {**tk,**message}
                            return jsonify(response)
                
                elif missing_token(request.args['username']):
                        nuovo_token={}
                            
                        nuovo_token['username']=request.args['username']
                        nuovo_token['token']= secrets.token_hex(16)
                        nuovo_token['data']=time.time()
                            
                        token.append(nuovo_token)
                        
                        message = {'message' : '''IL TOKEN E' STATO CREATO PER LA PRIMA VOLTA: ASSEGNAZIONE TOKEN RIUSCITA'''}
                        response = {**nuovo_token,**message}    
                        return jsonify(response)
                                    
                else:
                    
                    for tk in token:
                        if request.args['username']==tk['username']:
                            
                            message={'message': '''<h2> L'UTENTE HA ANCORA IL TOKEN VALIDO </h2>'''}
                            response= {**tk,**message}
                            
                            return jsonify(response)
                                    
        else:
                        return ('''<h2> PASSWORD ERRATA </h2>''')
        
    else:                               
                        return ('''<h2>L'UTENTE NON E' REGISTRATO</h2>''')




@app.route('/api/v1/resources/invio', methods=['POST'])

def send():
    
    lista_utenti = update_lista_utenti(utenti_registrati)
    
    if request.args['destinatario'] not in lista_utenti.keys():
        
        return ''' <h1> Il Destinatario non esiste </h1>'''

    elif token_scaduto(request.args['username']):
        
        return ''' <h1>Sessione scaduta, effetuare autenticazione</h1> '''
    
    elif token_errato(request.args['username'],request.args['token']):
        
        return '''<h1>il token inserito non è valido</h1>'''

    else :
    
        nuovo_messaggio = {}
        
        #salvataggio messaggio database messaggi
        
        nuovo_messaggio['mittente'] = request.args['username']
        
        nuovo_messaggio['destinatario'] = request.args['destinatario']
        
        nuovo_messaggio['messaggio'] = request.args['messaggio']
        
        #nuovo_messaggio['data'] = request.args['timestamp']
        
        nuovo_messaggio['data'] = time.time()
        
        nuovo_messaggio['messaggio_consegnato'] = False
        
        
        messaggi.append(nuovo_messaggio)
        
        return 'messaggio inviato con successo: {}'.format(nuovo_messaggio['messaggio'])

@app.route('/api/v1/resources/ricevi', methods=['GET'])
def receive():
    
    lista_utenti = update_lista_utenti(utenti_registrati)
    
    if token_scaduto(request.args['username']):
        
        return ''' <h1>Sessione scaduta, effetuare autenticazione</h1> '''
    
    elif token_errato(request.args['username'], request.args['token']):
        
        return ''' <h1>il token inserito non è valido</h1> '''
    
    else: #sessione valida
        
        messaggi_ricevuti = []
        
        for messaggio in messaggi:
            
            if request.args['username'] == messaggio['destinatario'] and messaggio['messaggio_consegnato'] == False:
                
                messaggi_ricevuti.append(messaggio)
                
                messaggio['messaggio_consegnato'] = True
    
        if messaggi_ricevuti == []:
            
            
            messaggio= {'message': ''' <h1> Non ci sono nuovi messaggi </h1>'''}
            messaggi_ricevuti['messaggio']=messaggi_ricevuti
            response= {**messaggio, **messaggi_ricevuti}
            
            return jsonify(response)
        
        else:
            
            return jsonify( messaggi_ricevuti)



@app.route('/api/v1/resources/utenti_registrati/all', methods=['GET'])
def utenti_all():
    return jsonify(utenti_registrati)




















