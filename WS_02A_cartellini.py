'''
Created on 16/nov/2012
           14/giu/2013 deriva da WS_01 (query), questa versione tenta INSERT

@author: Massi
'''
from suds.client import Client
import base64
import os
import time
#
#url = 'http://192.168.1.194:8080/adiJed/services/AdiJedWS?WSDL'
url = 'http://89.118.35.235:8080/adiJed/services/AdiJedWS?WSDL'
#url = 'http://172.31.1.162:8080/adiJed/services/AdiJedWS?WSDL'
print str(url)
#
client = Client(url)

print "Client: ", str(client)
#
temp = str(client)
print "Temp: ", str(temp)
#
print "Mi autentico e prelevo il token per la sessione.."
sessione = client.service.remoteLogin('immission','immission')
print "Fatto."
#print "getFam..."
# ADIJED--> 192.168.1.194/89.118.35.235 print client.service.getFam(sessione, 'cartellini')
print client.service.getFam(sessione, 'Cartellini')

#
indici = client.factory.create('tns:ArrayOfInt')
indici.int = 1021, 1019, 1020  #ID Serial Number, AVR, EQ
# ADIJED--> 172.31.1.162 indici.int = 1031, 1032, 1033  #ID Serial Number, AVR, EQ
#
ctr=1
#
valori = client.factory.create('tns:ArrayOfString')
base = "c:/ADIUTO/CARTELLINI_TEST/"
#
dirlist = os.listdir(base)
for cartellino in dirlist:
    print " "
    print "\nSto elaborando: ", cartellino
    #
    serial, req, avr1 = cartellino.split("_", 2)
    avr,  dummy       = avr1.split(".", 1)
    #valori.string = '0001683663', 'REQ0324998', 'AVR2050286'
    valori.string = serial, avr, req
    print "Serial: ", serial, "        AVR: ", avr, "      REQ: ", req
    #
    print "Carico file da allegare in memoria.."
    #body_file = open("c:/ADIUTO/CARTELLINI/0001683663_REQ0324998_AVR2050286.jpg", 'rb')
    body_file = open(base+cartellino, 'rb')
    body_data = base64.b64encode(body_file.read()) 
    print "Caricamento finito"
    print "Eseguo Insert: ", str(ctr)
    ctr=ctr+1
    client.service.insertDocument(sessione, body_data, cartellino, 1006, indici, valori)
    #ADIJED 172.31.1.162 client.service.insertDocument(sessione, body_data, cartellino, 1009, indici, valori)
    #print "Valori: ", valori
    #print "Indici: ", indici
    print "Insert eseguita."
    time.sleep(0)
#
print "Faccio logout...."
client.service.remoteLogout(sessione)
print "F I N I T O"