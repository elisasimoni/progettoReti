# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import threading
import sys, signal
import http.server
import socketserver
import requests
import cgi
from flask import request

#new imports


#manage the wait witout busy waiting
wait_refresh = threading.Event()
#scelta porta
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 9000
  
x=0
  


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
    <div align="left" class="list">
        <ul>
            <br>
            <li>
                <a href="http://127.0.0.1:{port}/rianimazione.html">
                    <h3>Rianimazione</h3>
                    <p>La rianimazione e' la branca della medicina che si occupa del paziente in condizioni critiche e della cura e del ripristino delle funzioni vitali compromesse dall'insorgenza di una malattia acuta o di un evento traumatico.</p>
                </a>
            </li>
            <br>
            <li>
                <a href="http://127.0.0.1:{port}/cardiologia.html">
                    <h3>Cardiologia</h3>
                    <p>La cardiologia e' quella branca della medicina interna che si occupa dello studio, della diagnosi e della cura (farmacologica e/o invasiva) delle malattie cardiovascolari acquisite o congenite.</p>
                </a>
            </li>
            <br>
            <li>
                <a href="http://127.0.0.1:{port}/dermatologia.html">
                    <h3>Dermatologia</h3>
                    <p>La dermatologia (dal greco derma, pelle) e' la branca della medicina che si occupa delle patologie a carico della pelle e degli annessi cutanei (peli, capelli, unghie, ghiandole sudoripare).</p>
                </a>
            </li>
            <br>
            <li>
                <a href="http://127.0.0.1:{port}/ginecologia.html">
                    <h3>Ginecologia</h3>
                    <p>La ginecologia e' una branca della medicina che si occupa talvolta della fisiologia, ma soprattutto della patologia inerenti all'apparato genitale femminile.</p>
                </a>
            </li>
            <br>
           <li>
                <a href="http://127.0.0.1:{port}/medicina_sport.html">
                    <h3>Medicina sportiva</h3>
                    <p>La medicina dello sport, conosciuta anche come medicina dello sport e dell'esercizio fisico, e' una branca della medicina che si occupa dello sport, dell'esercizio fisico e delle patologie ad essi correlate.</p>
                </a>
            </li>
            <br>
            <li>
                <a href="http://127.0.0.1:{port}/nefrologia.html">
                    <h3>Nefrologia</h3>
                    <p>La nefrologia e' quella branca della medicina interna che si occupa delle malattie renali.</p>
                </a>
            </li>
            <br>
            <li>
                <a href="http://127.0.0.1:{port}/neurologia.html">
                    <h3>Neurologia</h3>
                    <p>La neurologia e' la branca specialistica della medicina che studia le patologie del sistema nervoso centrale , del sistema periferico somatico e del sistema nervoso periferico autonomo .</p>
                </a>
            </li>
            <br>
            <li>
                <a href="http://127.0.0.1:{port}/oculista.html">
                    <h3>Oculista</h3>
                    <p>Un oculista e' un medico che ha anche conseguito il titolo di specialista in oftalmologia.</p>
                </a>
            </li>
            <br>
            <li>
                <a href="http://127.0.0.1:{port}/oncologia.html">
                    <h3>Oncologia</h3>
                    <p>L'oncologia e' il ramo della medicina che studia i tumori dal punto di vista morfologico e clinico.</p>
                </a>
            </li>
            <br>
           <li>
                <a href="http://127.0.0.1:{port}/ortopedia.html">
                    <h3>Ortopedia</h3>
                    <p>L'ortopedia e' una branca iperspecialistica della chirurgia che si occupa dello studio e del trattamento delle patologie dell'apparato locomotore.</p>
                </a>
            </li>
            <li>
                <a href="http://127.0.0.1:{port}/otorino.html">
                    <h3>Otorino</h3>
                    <p>L'otorinolaringoiatria e' la branca della medicina che si occupa di prevenzione, diagnosi e terapia sia medica sia chirurgica delle patologie del distretto testa-collo, ossia dell'orecchio (udito ed equilibrio), del naso (respirazione e apnee del sonno) e della gola</p>
                </a>
            </li>
            </li> <a href="http://127.0.0.1:{port}/Servizi_offerti.pdf" download="Servizi_offerti.pdf">Download lista servizi</a></li>
        </ul>
        <br>
   </div>
""".format(port=port)

page_style = """
<style>
    * {margin: 0; padding: 0;}
 
    div {
        margin: 20px;
    }
 
    ul {
        list-style-type: none;
        width: 500px;
    }
 
    h3 {
        font: bold 20px/1.5 Helvetica, Verdana, sans-serif;
    }
 
    li p {
        font: 200 12px/1.5 Georgia, Times New Roman, serif;
    }
 
    li {
        float: left;
        margin: 0 15px 0 0;
        padding: 10px;
        overflow: auto;
    }
 
    li:hover {
        background: #eee;
        cursor: pointer;
    }
    
    .list a {
        color: black;
        text-decoration: none;
    }
</style>
"""

login_style = """
<style>
    form {
        border: 3px solid #f1f1f1;
    }
    input[type=text], input[type=password] {
        width: 50%;
        padding: 12px 20px;
        margin: 8px 0;
        display: inline-block;
        border: 1px solid #ccc;
        box-sizing: border-box;
    }
    
    button {
        background-color: #04AA6D;
        color: white;
        padding: 12px 20px;
        margin: 8px 0;
        border: none;
        cursor: pointer;
        width: 50%;
    }
</style>
"""

center_page = """ 
<body>  
    <center> <h1> Login Form </h1> </center> 
    <form method="POST">
        <h3 align="center">Login</h3>
        <div class="form-group">
            <label for="username">Username</label>
            <input
                type="text"
                class="form-control"
                id="username"
                name="username"
                placeholder="Enter username"
        />
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input
                type="password"
                class="form-control"
                id="password"
                name="password"
                placeholder="Enter password"
            />
        </div>
            <button type="submit" class="btn btn-primary" name="login" value="login">Submit</button>
            <br>
            <a href="http://127.0.0.1:{port}/registrer.html">Sign Up</a>
        </div> 
        </div>
    </form>   
""".format(port=port)

center_page2 = """ 
<body>  
    <form method="POST">
        <h3 align="center">Sign Up</h3>
        <div class="form-group">
            <label for="username">Username</label>
            <input
                type="text"
                class="form-control"
                id="username"
                name="username"
                placeholder="Enter username"
        />
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input
                type="password"
                class="form-control"
                id="password"
                name="password"
                placeholder="Enter password"
            />
        </div>
        <div class="form-group">
            <label for="password2">Password (confirm)</label>
            <input
                type="password"
                class="form-control"
                id="password2"
                name="password2"
                placeholder="Confirm password"
            />
    </div>
    <br />
    <button type="submit" class="btn btn-primary" name="registrazione">Submit</button>
    </form>  
"""


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
   
    def do_POST(self):
        try:
            # Salvo i vari dati inseriti
            form = cgi.FieldStorage(    
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'})
            global x
            
            # Con getvalue prendo i dati inseriti dall'utente
            if x == 0:
                username = form.getvalue('username')
                password = form.getvalue('password')
                f=open("credential.txt","r")
                lines = f.readlines()
                print(len(lines))
                print(username+"\n"+password)
                i=0
                while i < len(lines):
                    print("sono entrato")
                    if lines[i].strip() == username and lines[i+1].strip() == password:
                        print("okkk")
                        self.path='home.html'
                        return http.server.SimpleHTTPRequestHandler.do_GET(self)
                    i+=2
                print("sono uscito")
                print(self.path)
                self.path='registrer.html'
                x=1
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            elif x==1:
                username=form.getvalue('username')
                password = form.getvalue('password')
                password2 = form.getvalue('password2')
                if password == password2:
                    with open("credential.txt", "a") as out:
                        info = "\n"+username + "\n" + password
                        out.write(info)
                        x=0
                        self.path='autenthication.html'
                        return http.server.SimpleHTTPRequestHandler.do_GET(self)
                self.path='registrer.html'
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            # Stampo all'utente i dati che ha inviato
            self.send_response(200)
        except: 
            self.send_error(404, 'Bad request submitted.')
            return;
        
        self.end_headers()
        
        # Salvo in locale i vari messaggi in AllPOST
          
         
# ThreadingTCPServer per consentire l'accesso a più utenti in contemporanea
server = socketserver.ThreadingTCPServer(('127.0.0.1',port),requestHandler)
print("Server running on port %s" % port)  


def autenthication_page():
    f = open("autenthication.html",'w', encoding="utf-8")  
    message = header_html+login_style+center_page+footer_html
    f.write(message)
    f.close()

def registrer_page():
    f = open("registrer.html",'w', encoding="utf-8")  
    message = header_html+login_style+center_page2+footer_html
    f.write(message)
    f.close()

def home_page():
    f = open("home.html",'w', encoding="utf-8")  
    message = header_html+page_style+link_center+footer_html
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
    registrer_page()
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
