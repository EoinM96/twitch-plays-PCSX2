"""
Twitch plays PCSX2 chat control setup
"""

# import time
import socket
import pyautogui
import threading


# User specific variables
PASS = 'INSERT YOUR TWITCH AUTHORIZATION CODE HERE'
PORT = 6667
CHANNEL = "INSERT TWITCH CHANNEL NAME HERE"
OWNER = "INSERT TWITCH CHANNEL NAME HERE"

# Static variables
SERVER = "irc.twitch.tv"
BOT = "TwitchBot"
message = ""
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(("PASS " + PASS + "\n" +
          "NICK " + BOT + "\n" +
          "JOIN #" + CHANNEL + "\n").encode())


def gameControl():
    global message

    # Waittime can be added between key down/up to keep key continually pressed
    # waittime = 0.4

    # Basic controller controls can be added/ammended below
    # PCSX2 maps PS2 controll buttons to keys on keyboard
    # Here we map messages from chat to keys on the keyboard
    # See your own PCSX2 controller configuration for button mapping details
    while True:
        if "up" in message.lower():
            pyautogui.keyDown('w')
            # time.sleep(waittime)
            message = ""
            pyautogui.keyUp('w')
        elif "down" in message.lower():
            pyautogui.keyDown('s')
            # time.sleep(waittime)
            message = ""
            pyautogui.keyUp('s')
        elif "left" in message.lower():
            pyautogui.keyDown('a')
            # time.sleep(waittime)
            message = ""
            pyautogui.keyUp('a')
        elif "right" in message.lower():
            pyautogui.keyDown('d')
            # time.sleep(waittime)
            message = ""
            pyautogui.keyUp('d')
        elif "x" in message.lower():
            pyautogui.keyDown('down')
            # time.sleep(waittime)
            message = ""
            pyautogui.keyUp('down')
        elif "square" in message.lower():
            pyautogui.keyDown('left')
            # time.sleep(waittime)
            message = ""
            pyautogui.keyUp('left')
        elif "circle" in message.lower():
            pyautogui.keyDown('right')
            # time.sleep(waittime)
            message = ""
            pyautogui.keyUp('right')
        elif "triangle" in message.lower():
            pyautogui.keyDown('up')
            # time.sleep(waittime)
            message = ""
            pyautogui.keyUp('up')
        else:
            pass


def twitch():
    # Link with twitch chat
    def joinchat():
        loading = True
        while loading:
            readbuffer_join = irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                loading = loadingComplete(line)

    # Publish message to twitch chat when code is running
    def loadingComplete(line):
        if "End of /NAMES list" in line:
            print("Code is live!")
            sendMessage(irc, "Code is live!")
            return False
        else:
            return True

    # Send message function
    def sendMessage(irc, message):
        messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
        irc.send((messageTemp + "\n").encode())

    # Get user name from incoming message
    def getUser(line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    # Get message body from incoming message
    def getMessage(line):
        global message
        try:
            message = (line.split(":", 2))[2]
        except:
            message = ""
        return message

    def Console(line):
        if "PRIVMSG" in line:
            return False
        else:
            return True

    joinchat()

    # Read for incoming messages
    while True:
        try:
            readBuffer = irc.recv(1024).decode()
        except:
            readBuffer = ""

        for line in readBuffer.split("\r\n"):
            if line == "":
                continue
            elif "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                irc.send(msgg)
                continue
            else:
                print(line)
                user = getUser(line)
                message = getMessage(line)
                print(user + " : " + message)


# Run program as main in threading mode
if __name__ == '__main__':
    t1 = threading.Thread(target=twitch)
    t1.start()
    t2 = threading.Thread(target=gameControl)
    t2.start()
