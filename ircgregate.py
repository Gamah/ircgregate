import sys
import socket
import string
import re
import os
 
HOST = "changeme"
PORT = 6667
 
NICK = "changeme"
IDENT = "changeme"
REALNAME = "changeme"
CHANNEL = "#changeme"
MYSQLU = "changeme"
MYSQLP = "changeme"

#make a buffer of text
readbuffer = ""

#open a connection
s=socket.socket( )
s.connect((HOST, PORT))

#identify to the server
s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))

#database insert
def dbi(s,m):
    #exclude known bot
    if(s != "JBot"):
        for word in m.split():
            #don't insert words over 15 characters
            if(len(word) < 15):
                os.system("mysql --user=%s --password=%s -e \"INSERT INTO ircgregate.swagdata(user,word,timestamp) VALUES('%s','%s',now())\"" % (MYSQLU, MYSQLP, s, word))

while 1:
    #dump the buffer if it's getting to big
    if(len(readbuffer) >= 2048):
        readbuffer = ""
    readbuffer = readbuffer+s.recv(1024).decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop( )
    #process the newest line
    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)
        print(line)
        #avoid getting kicked from the server
        if(line[0] == "PING"):
            s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        else:
            #if MOTD is complete, we can join a channel
            if(line[1] == "376"):
                s.send(bytes("JOIN %s \r\n" % (CHANNEL), "UTF-8"));
            #if message was sent to channel, figure out who sent it, and what it is.
            if(line[2] == CHANNEL):
                sender = ""
                for char in line[0]:
                    if(char == "!"):
                        break
                    if(char != ":"):
                        sender += char 
                size = len(line)
                i = 3
                message = ""
                while(i < size): 
                    message += line[i] + " "
                    i = i + 1
                message.lstrip(":")
                #remove scary characters to prevent sql/shell injection
                message = re.sub(r'\W+', ' ', message)
                #no need to insert blank messages into the DB
                if(message != ""):
                    #assuming the message was sent to the channel, make sure it was actually a message and not a join/leave/kick/etc command
                    if(line[1] == "PRIVMSG"):
                        dbi(sender,message)
                    #print sender and message for debugging
                    print(sender + "\r\n" + message)
