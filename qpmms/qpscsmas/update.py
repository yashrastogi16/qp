from sys import stdin, exc_info
from time import sleep
import datetime
import socket
import MySQLdb
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
#import serial, binascii
import win32api; 
import win32ui
import time
from datetime import date
breakfast_start = datetime.time(8,00,00,0000)
breakfast_end = datetime.time(10,00,00,0000)
lunch_start = datetime.time(14,00,00,0000)
lunch_end = datetime.time(16,00,00,0000)
dinner_start = datetime.time(19,00,00,0000)
dinner_end = datetime.time(21,30,00,0000)

# import easygui

conn = MySQLdb.connect(host= "127.0.0.1",
                  user="root",
                  password="1234",
                  db="qpscsmas")
x = conn.cursor()                  
                 
class printobserver(CardObserver):
    def update(self, observable, (addedcards, removedcards)):
        cr = CardRequest(timeout=100000000000, newcardonly=True)
        cs = cr.waitforcard()
        cs.connection.connect()
        response, sw1, sw2 = cs.connection.transmit( [0xFF, 0xCA, 0x00, 0x00, 0x00] )
        self.tagid = toHexString(response).replace(' ','')
        id = self.tagid
        print "ID ID THIS",id
        c=id.lower()
        # print c
        d=socket.gethostbyname(socket.gethostname())
        now = datetime.datetime.now()
        print "time",datetime.datetime.now()
        if breakfast_start <= datetime.datetime.now().time() <= breakfast_end:
            print "Break fast"
            x.execute (" INSERT INTO qpscsmas_emp_breakfast(`rfidcardno`,breakfast_count, date_time) VALUES ('%s',1,'%s')"%(c,now) )
            conn.commit()
        if lunch_start <= datetime.datetime.now().time() <= lunch_end:
            print "lunch"
            x.execute (" INSERT INTO qpscsmas_emp_lunch(`rfidcardno`,lunch_count, date_time) VALUES ('%s',1,'%s')"%(c,now) ) 
            conn.commit()       
        if dinner_start <= datetime.datetime.now().time() <= dinner_end:
            print "Dinner time"
            x.execute (" INSERT INTO qpscsmas_emp_dinner(`rfidcardno`,dinner_count,date_time) VALUES ('%s',1,'%s')"%(c,now) ) 
            conn.commit()
        else:
            print "This is the not time for food"
        # q = "select rfidcardno from qpcmms_member"
        # x.execute(q)          
        # result=[item[0] for item in x.fetchall()] 
        # # print result
        # if result:
            # if id.lower() in result:                  
                # q = "SELECT * from qpcmms_member WHERE rfidcardno = '%s'" % (id,)           
                # x.execute(q)
                # t = x.fetchone()   
                # # print "tT", t, t[1]           
                # if 'Active' in t:
                    # easygui.msgbox(t[1] +" You are Welcome")
                # elif 'Pending' in t:
                    # easygui.msgbox(t[1] + " Your Status is  " +t[8])
                # elif 'Suspend' in t:
                    # easygui.msgbox(t[1] +" You are Suspended ")
                # else:
                    # easygui.msgbox("Sorry Access denied")
        # qf = "select rfidcardno from qpcmms_family"
        # x.execute(qf)          
        # resultf=[item[0] for item in x.fetchall()] 
        # if resultf:
            # if id.lower() in resultf:  
                # q = "SELECT status, name from qpcmms_family WHERE rfidcardno = '%s'" % (id,)           
                # x.execute(q)
                # cl=[item[0:] for item in x.fetchone()] 
                
                # if cl[0] == 'Active':
                    # easygui.msgbox(cl[1] +"  You are Welcome " )
                # elif cl[0] == 'Pending':
                    # easygui.msgbox(cl[1] +" Your Status is  " +cl[0])
                # elif cl[0] == 'Suspend':
                    # easygui.msgbox(cl[1] +" You are Suspended ")
                # else:
                    # easygui.msgbox("Sorry Access denied")
        # if id.lower() not in result and id.lower() not in resultf:
             # easygui.msgbox("Sorry Access denied")
        
        import time
        for i in range(len(id)):
            test = ord(id[i])
            win32api.keybd_event(test, i, )
        cs.connection.disconnect()
try:
    cardmonitor = CardMonitor()
    cardobserver = printobserver()
    cardmonitor.addObserver(cardobserver)
    import sys
    if 'win32' == sys.platform:
        print 'press Enter to continue'
        sys.stdin.read(1)
except:
    print exc_info()[0], ':', exc_info()[1]
