import socketio, pyno, ansi, time, os

socket = socketio.Client()
messages = []

global typing
typing =[]

global inp, name, color
inp = ""
name = ""
color = ""

def push(message): socket.emit("push", message)

def connect(uri, name):
    socket.connect(uri)
    push(["join", name+" has joined the chat"])

def disconnect(name): push(name+" has left the chat")

def formatTyping(typing):
    if len(typing) == 0: return ""
    elif len(typing) == 1: return "".join(typing)+" is typing"
    else: return ", ".join(typing)+" are typing"

def drawScreen(typing, inp):
    os.system("clear")
    print("\n".join(messages)+"\n\n"+formatTyping(typing)+"\n"+inp+ansi.hidecursor)

@socket.event
def recvMessage(message, sid):
    if message[0] == "typing status":
        typer, status = message[1][0], message[1][1]
        if status == True: typing.append(typer)
        else: typing.remove(typer)
    elif message[0] == "chat":
        messages.append(message[1])
        if len(messages) > 100: del messages[0]
        if str("@"+name) in message: 
            strippedName = message.split(": ")
            del strippedName[1]
            pyno.notify("".join(strippedName).split("m")[1]+" mentioned you",message.split(": ")[1].replace("[38;5;"+color,"").replace("[38;5;3m","").replace("[0m",""),"default")
    elif message[0] == "join":
        messages.append(message[1])
        pyno.notify(message[1],message[1],"default")
    drawScreen(typing, inp)

def passTypers():
    return typing

def getMessages(): return(messages)

def passInp(var):
    global inp
    inp = var

def passName(var):
    global name
    name = var

def passColor(var):
    global color
    color = var