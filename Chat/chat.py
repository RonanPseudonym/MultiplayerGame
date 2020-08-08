print("Starting up...")

import wsm, ansi, atexit, time, getch, os, random, styles

blacklist = "␛"

hostname = input("Enter name: ").strip().replace(" ","-").replace("_","-").replace("@","").replace("*","").replace("`","").lower()
color = str(random.randint(1, 230))+"m"

inp = ["> "]

wsm.passInp("".join(inp))

print("Connecting...")

while True:
    try: 
        wsm.connect("ws://Black-Sun.ronanpseudonym.repl.co", hostname)
        break
    except:
        print("Waking server...")
        time.sleep

typing = False

try: 
    while True:
        inp = ["> "]
        while True: 
            oldTyping = typing
            key = getch.getch()
            if key == "\n": 
                wsm.passInp("> ▉")
                typingStatus = False
                break
            elif key == "backspace": 
                if len(inp) > 2: del inp[-1]
                elif len(inp) <= 2:
                    typing = False
                    if len(inp) == 2: del inp[-1]
            elif not key in blacklist: 
                inp.append(key)
                typing = True
            wsm.passInp("".join(inp)+"▉")
            os.system("clear")
            wsm.drawScreen(wsm.passTypers(), "".join(inp)+"▉")
            if oldTyping != typing:
                oldTyping = typing
                wsm.push(hostname+" typing status: "+str(typing))
        typing = False
        if oldTyping != typing:
            oldTyping = typing
            wsm.push(hostname+" typing status: "+str(typing))
        del inp[0]
        closeBold = False
        closeItalic = False
        closeMono = False
        for i in range(0, len(inp)):
            searching = ""
            if inp[i] == "@":
                inp[i] = ansi.color+"3m"+inp[i]
            elif inp[i] == " ":
                inp[i] = ansi.color+color+inp[i]
            elif inp[i] == "*":
                closeBold = not closeBold
                if closeBold == True: inp[i] = ansi.bold
                else: inp[i] = ansi.esc+ansi.color+color
            elif inp[i] == "_":
                closeItalic = not closeItalic
                inp[i] = ""
            elif inp[i] == "`":
                closeMono = not closeMono
                inp[i] = ""
            elif closeItalic == True:
                if inp[i] in list(styles.normal): inp[i] = str(styles.italic[list(styles.normal).index(inp[i])])
            elif closeMono == True:
                if inp[i] in list(styles.normal): inp[i] = str(styles.mono[list(styles.normal).index(inp[i])])
        if len(inp) > 0: wsm.push("␛ "+ansi.color+color+hostname+": "+"".join(inp).strip()+ansi.esc)

except KeyboardInterrupt: wsm.disconnect(hostname)