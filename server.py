# Echo server program
import socket
import sys, os
import time
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
import logging


logging.basicConfig()


Host = None
hosts_open ={}
hosts_status={}

HOST = 'localhost'               # Symbolic name meaning all available interfaces
PORT = 52645              # Arbitrary non-privileged port
s = None

def set_RHOST(Lhost):
    global HOST
    HOST = Lhost

def set_RPORT(Rport):
    global PORT
    PORT = Rport

def list_hosts_open():
    i=1
    if len(hosts_open) == 0:
        print "No Open Host"
    else:
        for host in hosts_open:
            print str(i) + "- " + host
            i +=1

def list_hosts_info():
    i=1
    if len(hosts_open) == 0:
        print "No Open Host"
    else:
        for host in hosts_status:
            print str(i) + "- " + str(hosts_status[host])


def send_request(host):
    if host is not None:
        global Host
        Host = host

def program_menu():
    abc = 0
    while 1:
        print "Menu --------"
        print "1- List Open Hosts"
        print "2- Send Request"
        print "3- Delete Host"
        print "4- List Open Hosts Information"
        print "5- Exit"
        abc = int(float(raw_input("Select a Menu Option!!\r\n")))
        if abc == 1:
            list_hosts_open()
        elif abc == 2:
            send_request(raw_input("Enter Host!!!"))
        elif abc == 4:
            list_hosts_info()
        elif abc == 5:
            os._exit(52645)
        else:
            print "There is no option like this!"


def listen(s ):
    while 1:
        if s is None:
            print 'could not open socket'
        #addr -- address of connect
        conn, addr = s.accept()

        try:
            data = conn.recv(1024)
            if not data: break
            if data == "update":
                ip_address = str(addr).split(",")[0]
                hosts_open[ip_address] = time.strftime("%m%d%H%M%S",time.localtime())
                global Host
                if Host != None:
                    conn.send("ping "+Host)
                    Host = None
                else:
                    conn.send("okay")
                    data = conn.recv(1024)
                    hosts_status[ip_address] = data
        except socket.error as msg:
            s.close()
            s = None
            continue

        conn.close()


def control_hosts():
    time_stamp = float(str(time.strftime("%Y%m%d%H",time.localtime())))
    for host in hosts_open.keys():
        if float(str(hosts_open[host])) <= time_stamp + 300 :
            del hosts_open[host]
            print "Lost connection with " + host


for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break




threads = []


temp1 = threading.Thread(target=program_menu)
temp2 = threading.Thread(target=listen,args=(s,))
threads.append(temp1)
threads.append(temp2)
for thread in threads:
    thread.start()

#scheduler for sending update
scheduler = BlockingScheduler()
scheduler.add_job(control_hosts, 'interval', minutes=2)
scheduler.start()



