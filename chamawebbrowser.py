import time
import subprocess
import webbrowser

url = "http://10.2.105.115:8080/LinhaInfoWeb/"
webbrowser.open(url)
time.sleep(10)
subprocess.call(["xdotool", "key", "F11"])
