# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import threading
import urllib.request
import sys, signal
import http.server
import socketserver
import requests
from bs4 import BeautifulSoup
#new imports


content = "CIAO"

#manage the wait witout busy waiting
wait_refresh = threading.Event()

#scelta porta
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8080
  
header_html = """
<html>
    <head>
        
       
"""

link_center = """
<title >Servizi Ospedalieri</title>
<body>
<H1 align="center">
    Servizi Ospedalieri Nardini e Simoni
</H1>
    <div align="center">
       <p>
            
            <a href="http://127.0.0.1:{port}">Home</a>
  		    <a href="http://127.0.0.1:{port}/rianimazione.html">Rianimazione</a>
            <a href="http://127.0.0.1:{port}/ortopedia.html">Ortopedia</a>
            <a href="http://127.0.0.1:{port}/ginecologia.html">Ginecologia</a>
            <a href="http://127.0.0.1:{port}/cardiologia.html">Cardiologia</a>
            <a href="http://127.0.0.1:{port}/otorino.html">Otorinolarigoiatria</a>
            <a href="http://127.0.0.1:{port}/neurologia.html">Neurologia</a>
            <a href="http://127.0.0.1:{port}/oculista.html">Oculista</a>
            <a href="http://127.0.0.1:{port}/dermatologia.html">Dermatologia</a>
            <a href="http://127.0.0.1:{port}/oncologia.html">Oncologia</a>
            <a href="http://127.0.0.1:{port}/medicina_sport">Medicina dello sport</a>
            <a href="http://127.0.0.1:{port}/nefrologia.html">Nefrologia</a>
  		    
            <a href="http://127.0.0.1:{port}/lista_servizi.pdf" download="lista_servizi.pdf">Download lista servizi</a>
  		</p>
   </div>
""".format(port=port)

center_page = """ <title >Servizi Ospedalieri</title> <body> <H1 align="center">
    """ + content +  """</H1>""".format(port=port)

footer_html= """
    </body>
</html>
"""  
  
  
class requestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
       self.send_response(200)
       # Specifichiamo uno o più header
       self.send_header('Content-type','text/html')
       self.end_headers() 
       message = header_html+link_center+footer_html
       self.wfile.write(bytes(message, "utf8"))
       return
       
        
         
# ThreadingTCPServer per consentire l'accesso a più utenti in contemporanea
server = socketserver.ThreadingTCPServer(('127.0.0.1',port),requestHandler)
print("Server running on port %s" % port)       


#creo una funzione per creare le pagine dei vari servizi
def service_page(name, url):
    f = open(name + ".html",'w', encoding="utf-8")  
    try:
         message = header_html+center_page+footer_html
    except:
        pass
    f.write(message)
    f.close()

#carico le pagine 
def load_page():
    cardiologia_page()
    neurologia_page()
    otorino_page()
    oculista_page()
    nefrologia_page()
    ginecologia_page()
    ortopedia_page()
    rianimazione_page()
    medicina_sport_page()
    oncologia_page()
    dermatologia_page()    


        
def cardiologia_page():
    service_page("cardiologia","https://www.auslromagna.it/organizzazione/dipartimenti/cardiovascolare/cardiologia-forli")
def neurologia_page():
    service_page("neurologia","https://www.auslromagna.it/organizzazione/dipartimenti/internistico-forli-cesena/neurologia-ospedale-di-forli-cesena/neurologia-forli")
def otorino_page():
    service_page("otorino","https://www.auslromagna.it/organizzazione/dipartimenti/testa-collo/otorinolaringoiatria-forli")
def oculista_page():
    service_page("oculista","https://www.auslromagna.it/organizzazione/dipartimenti/testa-collo/oculistica-forli")
def nefrologia_page():
    service_page("nefrologia","https://www.auslromagna.it/organizzazione/dipartimenti/internistico-forli-cesena/nefrologia-dialisi-forli-cesena/nefrologia-dialisi-forli")
def ginecologia_page():
    service_page("ginecologia","https://www.auslromagna.it/organizzazione/dipartimenti/salute-donna-infanzia-adolescenza-forli-cesena/ostetricia-e-ginecologia-forli")
def ortopedia_page():
    service_page("ortopedia","https://www.auslromagna.it/organizzazione/dipartimenti/osteoarticolare/ortopedia-e-traumatologia-forli")
def rianimazione_page():
    service_page("rianimazione","https://www.auslromagna.it/organizzazione/dipartimenti/chirurgico-generale-forli/anestesia-e-rianimazione-forli")
def medicina_sport_page():
    service_page("medicina_sport","https://www.auslromagna.it/organizzazione/dipartimenti/dipsan/ambulatori-medicina-sport")
def oncologia_page():
    service_page("oncologia","https://www.auslromagna.it/organizzazione/dipartimenti/oncoematologico/prevenzione-oncologia-forli")
def dermatologia_page():
    service_page("anestesia","https://www.auslromagna.it/organizzazione/dipartimenti/chirurgico-grandi-traumi-cesena/centro-grandi-ustionati-dermatologia-cesena-forli/dermatologia-forli")


def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if(server):
        server.server_close()
    finally:
      #stop refresh
      wait_refresh.set()
      sys.exit(0)
def main():
   
    load_page()
    #L’interruzione da tastiera (o da console) dell’esecuzione
    #del web server deve essere opportunamente gestita in
    #modo da liberare la risorsa socket.
    server.daemon_threads = True 
    server.allow_reuse_address = True  
    signal.signal(signal.SIGINT, signal_handler)
    try:
      while True:
        server.serve_forever()
    except KeyboardInterrupt:
      pass
    server.server_close()

if __name__ == "__main__":
    main()

  
   
  
   


    
    
    
    
    
