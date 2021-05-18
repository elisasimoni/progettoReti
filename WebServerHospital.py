# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import threading
import sys, signal
import http.server
import socketserver
import urllib.request, urllib.error, urllib.parse
import requests

#new imports


content = "Autentificazione"

#manage the wait witout busy waiting
wait_refresh = threading.Event()

#scelta porta
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 9000


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
            <a href="http://127.0.0.1:{port}/medicina_sport.html">Medicina dello sport</a>
            <a href="http://127.0.0.1:{port}/nefrologia.html">Nefrologia</a>
  		    
            <a href="http://127.0.0.1:{port}/lista_servizi.pdf" download="lista_servizi.pdf">Download lista servizi</a>
  		</p>
   </div>
""".format(port=port)

center_page = """ 

<body>  
    <center> <h1> Student Login Form </h1> </center> 
    <form>
        <div align="center">
        <div class="container"> 
            <label>Username : </label> 
            <input type="text" placeholder="Enter Username" name="username" required>
            <label>Password : </label> 
            <input type="password" placeholder="Enter Password" name="password" required>
            <button type="button"><a href="http://127.0.0.1:{port}/home.html">Login</a></button>
            <input type="checkbox" checked="checked"> Remember me
            Forgot password? </a> 
        </div> 
        </div>
    </form>   

""".format(port=port)

footer_html= """
    </body>
</html>
"""  
  
  
class requestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
       self.send_response(200)
       #Specifichiamo uno o più header
       if self.path == '/':
            self.path = 'autenthication.html'
       return http.server.SimpleHTTPRequestHandler.do_GET(self)
         
# ThreadingTCPServer per consentire l'accesso a più utenti in contemporanea
server = socketserver.ThreadingTCPServer(('127.0.0.1',port),requestHandler)
print("Server running on port %s" % port)       

def autenthication_page():
    f = open("autenthication.html",'w', encoding="utf-8")  
    message = header_html+center_page+footer_html
    f.write(message)
    f.close()

def home_page():
    f = open("home.html",'w', encoding="utf-8")  
    message = header_html+link_center+footer_html
    f.write(message)
    f.close()

#creo una funzione per creare le pagine dei vari servizi
def service_page(name, url):
    resp = requests.get(url)
    f = open(name + ".html",'w', encoding="utf-8")
    f.write(resp.text)
    f.close()
   
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
    service_page("dermatologia","https://www.auslromagna.it/organizzazione/dipartimenti/chirurgico-grandi-traumi-cesena/centro-grandi-ustionati-dermatologia-cesena-forli/dermatologia-forli")

#carico le pagine 
def load_page():
    autenthication_page()
    home_page()
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


