# Chat_Server_asd2021
Progetto Didattico architetture dei sistemi distribuiti. Implementazione di un chat server

REGISTRAZIONE:
'/api/v1/resources/registration',methods=['POST']
- valori richiesti: 1) username 2) password
-possibili risposte:
1) se l'utente non è registrato viene restituito il dizionario contenente username, password e il messaggio di avvenuta registrazione;
2) se l'utente è gia registrato viene restituito il messaggio che avvisa l'utente che l'username inserito è gia registrato.

AUTENTICAZIONE:
'/api/v1/resources/authentication',methods=['GET']

- valori richiesti: 1) username 2) password
- possibili risposte:
1) se l'utente è già stato autenticato, ma il suo token è scaduto, viene restituito il dizionario contenente username, token, data di rilascio del token ed il messaggio che avvisa l'utente che il token è stato aggiornato e l'autenticazione è riusicta;
2) se l'utente non si è mai autenticato, viene restituito il dizionario contenente username, token, data di rilascio del token ed il messaggio che avvisa l'utente che il token è stato assegnato e l'autenticazione è riuscita;
3) se l'utente è già stato autenticato ed il suo token è ancora valido viene restituito il dizionario contenente username, token, data di rilascio del token ed il messaggio che avvisa l'utente che il suo token è ancora valido e l'autenticazione è riuscita;
4) se la password è errata viene restituito il messaggio che avvisa l'utente che la password è errata e l'autenticazione non è riuscita;
5) se l'utente non è registrato viene restituito il messaggio che avvisa l'utente di non essere registrato e l'autenticazione non è riuscita.

INVIO MESSAGGI:
'/api/v1/resources/send', methods=['POST']
- valori richiesti: 1) username 2) destinatario 3) token 4) messaggio
- possibili risposte:
1) se il destinatario non è registrato viene restituito il messaggio che avvisa l'utente che il destinatario non è registrato ed il messaggio non è stato inviato;
2) se il token è scaduto viene restituito il messaggio che avvisa l'utente di effettuare l'autenitcazione per poter inviare il messaggio;
3) se il token è errato viene restituito il messaggio che avvisa l'utente che il token è errato e il messaggio non è stato inviato;
4) se il token è valido ed il destinatario è registrato viene inviato all'utente il messaggio che lo avvvisa che l'invio del messaggio è avvenuto con successo.

RICEZIONE MESSAGGI:
'/api/v1/resources/receive', methods=['GET']
- valori richiesti: 1) username 2) token
- possibili risposte:
1) se l'utente ha il token scaduto viene restituito il messaggio che avvisa l'utente di effettuare l'autenticazione;
2) se l'utente ha inserito il token errato viene restituito il messaggio che avvisa l'utente che il token è errato;
3) se l'utente ha il token valido e non ha ricevuto nuovi messaggi viene restituito il dizionario vuoto ed il messaggio che avvisa l'utente che non ci sono messaggi;
4) se l'utente ha il token valido e ha ricevuto nuovi messaggi, viene restituo il dizionario contenente messaggio ricevuto, il mittente del messaggio e la data di invio del messaggio.

VISUALIZZAZIONE UTENTI REGISTRATI:
'/api/v1/resources/utenti_registrati/all', methods=['GET']
- viene restituita la lista degli utenti registrati


















###### ciao
