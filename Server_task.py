#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 17:59:08 2021

@author: francescaronci
"""
import flask
from flask import request, jsonify
import random



app = flask.Flask(__name__)

messaggi = [
    {
    'username': 'Marco',
    #'token': random.getrandbits(128),
    'destinatario': 'Laura',
    'messaggio': 'ciao',
    'data e ora': 12/03/2021 13:00:00
    },
    {
    'username': 'Paolo',
    #'token': random.getrandbits(128),
    'destinatario': 'Franca',
    'messaggio': 'come stai',
    'data e ora': 12/03/2021 14:00:00

    }
    ]

utenti_registrati= [
        {
            'username':'Marco',
            'password': 1234,
            'token': 'bdowb'
            }
        ]

@app.route('/api/v1/resources/registrazione',methods=['POST'])
def register():
   nuovo_utente= {}

   lista_utenti=[utenti_registrati[i]['username'] for i in range(len(utenti_registrati))]

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
def autentication():
        lista_utenti={utenti_registrati[i]['username']:utenti_registrati[i]['password'] for i in range(len(utenti_registrati))}

        if request.args['username'] in lista_utenti.keys():
            if int(request.args['password'])== lista_utenti[request.args['username']]:
                  return ('''<h2>AUTENTICAZIONE RIUSCITA </h2>''')
            else:
              return ('''<h2> PASSWORD ERRATA </h2>''')

        else:

            ('''<h2>L'UTENTE NON E' REGISTRATO</h2>''')




@app.route('//api/v1/resources/invio', methods=['POST'])
def send():
    return '''<h1>Database Studenti</h1>
    <p>Per accedere all'enenco studenti indicare il percorso /api/v1/resources/students/all'''

@app.route('/api/v1/resources/messaggi/all', methods=['GET'])
def mess_all():
    return jsonify(messaggi)

@app.route('//api/v1/resources/ricevi', methods=['GET'])
def receive():
    return '''<h1>Database Studenti</h1>
    <p>Per accedere all'enenco studenti indicare il percorso /api/v1/resources/students/all'''

@app.route('/api/v1/resources/utenti_registrati/all', methods=['GET'])
def utenti_all():
    return jsonify(utenti_registrati)






