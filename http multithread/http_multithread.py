# Importazione delle librerie le cui funzioni sono utilizzate nel programma
import sys, signal
import http.server
import socketserver

# Lettura da riga di comendo della porta su cui si vuole mettere in ascolto il server.
# Se non viene inserito da tastiera il numero di porta allora viene adottato quello di default,
# che per il protocollo HTTP è l'8080. 
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8080

# ThreadingTCPServer per gestire più richieste effettuate dai client.
server = socketserver.ThreadingTCPServer(('',port), http.server.SimpleHTTPRequestHandler)

#Assicura che da tastiera usando la combinazione
#di tasti Ctrl-C termini in modo pulito tutti i thread generati
#permettendo di attivare nuovamente il server sulla stessa porta senza
#dover attendere. Infatti, la porta una volta premuti i tasti Ctrl-C
#viene resa nuovamente accessibile dal sistema operativo.
server.daemon_threads = True  
#il Server acconsente al riutilizzo del socket anche se non è ancora stato
#rilasciato quello precedente, andandolo a sovrascrivere
server.allow_reuse_address = True  

#Definizione di una funzione che permette di uscire dal processo tramite 
#la pressione dei tasti Ctrl-C
def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if( server ):
        server.server_close()
    finally:
      sys.exit(0)

#interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
signal.signal(signal.SIGINT, signal_handler)

#Loop infinito per mantenere attivo il server fino a quando
#non avviene un'interruzione da tastiera.
try:
  while True:
    print("Server is starting on http://{}:{}".format('127.0.0.1', port))
    server.serve_forever()
except KeyboardInterrupt:
  pass

server.server_close()
