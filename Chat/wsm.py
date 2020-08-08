import socketio, pyno, ansi, time, os

socket = socketio.Client()
messages = []

global typing
typing =[]

global inp
inp = ""

def push(message): socket.emit("push", message)

def connect(uri, name):
    socket.connect(uri)
    push(name+" has joined the chat")

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
    if " typing status: " in message:
        typer, status = message.split(" typing status: ")
        if status == "True": typing.append(typer)
        else: typing.remove(typer)
    elif "␛" in message or "has joined the chat" in message:
        messages.append(message.replace("␛ ",""))
        if len(messages) > 100: del messages[0]
    drawScreen(typing, inp)

def passTypers():
    return typing

def getMessages(): return(messages)

def passInp(var):
    global inp
    inp = var