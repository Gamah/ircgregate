#!/usr/bin/env python

import sys
import socket
import string
import re
import os
import mysql.connector



HOST = "lucifer.geekshed.net"
PORT = 6667
 
NICK = "statbot"
IDENT = "statbot"
REALNAME = "statbot"
CHANNEL = "#jupiterbroadcasting"
 
CONNECTED = 0

readbuffer = ""

conn = mysql.connector.connect(user='root', password='swag', host='localhost', database='ircgregate', autocommit=True)
cur = conn.cursor()
cur.execute("SELECT NULL")
NULLCHECK = cur.fetchall()
def wordCheck(word):
    cur.execute("SELECT wordCheck(%s)", (word,))
    WORDID = cur.fetchall()
    if(WORDID != NULLCHECK):
        WORDID = WORDID[0]
        #print("word ", WORDID[0])
        return WORDID[0]
    else:
        if(word[:7] == "http://" or word[:4] == "www." or word[:8] == "https://"):
            cur.execute("INSERT IGNORE INTO words(word, type) VALUES(%s,1)", (word,))
        else:
            cur.execute("INSERT IGNORE INTO words(word, type, wordnochar) VALUES(%s,0,alphanum(%s))", (word,word))
        return wordCheck(word)
def userCheck(user):
    cur.execute("SELECT userCheck(%s)", (user,))
    USERID = cur.fetchall()
    if(USERID != NULLCHECK):
        USERID = USERID[0]
        #print("user ", USERID[0])
        return USERID[0]
    else:
        cur.execute("INSERT IGNORE INTO users(user) VALUES(%s)", (user,))
        cur.execute("SELECT userCheck(%s)", (user,))
        USERID = cur.fetchall()
        USERID = USERID[0]
        return userCheck(user)
def sentenceCheck():
    cur.execute("SELECT incSentence()")
    SID = cur.fetchall()
    SID = SID[0]
    return SID[0]
def transactionInsert(word, user, sentence):
    cur.execute("INSERT INTO transactions(idword,iduser,idsentence,timestamp) VALUES(%s, %s, %s, now())", (word, user , sentence))
def coolword(word):
    WORDID = wordCheck(word)
    cur.execute("UPDATE words SET isCool = 1 WHERE id = %s AND type = 0;", (WORDID,))
def makesmiley(word):
    WORDID = wordCheck(word)
    cur.execute("UPDATE words SET type = 2 where id = %s AND type = 0",(WORDID,))
      

s=socket.socket( )
s.connect((HOST, PORT))

s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))
#s.send(bytes("JOIN %s \r\n", % (CHANNEL) "UTF-8"));

def joinch(line):
    global CONNECTED
    if(line[1] == "005"):
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
    return (sender)

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
    sentenceID = sentenceCheck()
    userID = userCheck(user)
    for word in getmsg(line).split():
        wordID = wordCheck(word)
        transactionInsert(wordID,userID,sentenceID)
        

        
        
while 1:
    global CONNECTED
    readbuffer = readbuffer+s.recv(1024).decode("UTF-8",'ignore')
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop( )
    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)
        #print(line)
        if(line[0] == "PING"):
            s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        elif(CONNECTED == 0):
            joinch(line)
        else:
            if(line[2] == CHANNEL):
                print(getusr(line)+ ': ' + getmsg(line) + '\n')
                getwords(line)
            if(len(line) > 5 and line[2] == NICK and line[3] == ":suggest"):
                if(line[4] == "word"):
                    coolword(line[5])
                elif(line[4] == "smiley"):
                    makesmiley(line[5])
                else:
                    print("bad arg")
                print(line[5], " suggested as ", line[4])
