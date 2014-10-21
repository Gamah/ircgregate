import sys
import socket
import string
import re
import os
 
HOST = "irc.geekshed.net"
PORT = 6667
 
NICK = "statbott"
IDENT = "statbot"
REALNAME = "statbot"
CHANNEL = "#jupiterbroadcasting"
 
CONNECTED = 0

readbuffer = ""
 
s=socket.socket( )
s.connect((HOST, PORT))
 
s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))
#s.send(bytes("JOIN %s \r\n", % (CHANNEL) "UTF-8"));

def dbi(s,w):
    if(s != "Jbot"):
       # if(len(w) <= 50):
        os.system("mysql --user=root --password=swag -e \"INSERT INTO ircgregate.swagdata(user,word,timestamp) VALUES('%s','%s',now())\"" % (s, w))
def joinch(line):
    global CONNECTED
    if(line[1] == "376"):
        print("Connected! Joining channel")
        s.send(bytes("JOIN %s \r\n" % (CHANNEL), "UTF-8"));
        CONNECTED = 1

def getusr(line):
    sender = ""
    for char in line[0]:
        if(char == "!"):
            break
        if(char != ":"):
            sender += char
    return re.sub(r'[\W_]+', '',(sender))

def getmsg(line):
    size = len(line)
    i = 3
    message = ""
    while(i < size): 
        message += line[i] + " "
        i = i + 1
    message.lstrip(":")
    return message[1:]

def getwords(line):
    user = getusr(line)
    for word in getmsg(line).split():
        if(word[:7] == "http://"):
            word = "hyperlink posted"
        else:
            word = re.sub(r'[\W_]+', '',word)
        dbi(user,word)
        
while 1:
    global CONNECTED
    readbuffer = readbuffer+s.recv(1024).decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop( )
    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)
        print(line)
        if(line[0] == "PING"):
            s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        if(CONNECTED == 0):
            joinch(line)
        else:
            if(line[2] == CHANNEL):
                print(getusr(line))
                print(getmsg(line))
                getwords(line)
