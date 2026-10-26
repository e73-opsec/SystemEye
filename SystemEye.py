
from urllib.request import urlopen
import time
import os
import subprocess
import socket
import platform
import psutil
import uuid

os.system("clear")
time.sleep(1)

print('Welcome to my project SystemEye !')
time.sleep(0.5)
print(" ")
print("Tools: [1]wifi [2]ip [3]infos [4]wifi2 [5]mac [6]interface [7]ping [8]infos2 [9]disk [10]publicIP")
print(" ")
print("Useful tools: clear exit")

while True:
    user = input("~ ").strip().lower()
    if user == "1":
        time.sleep(0.3)
        print("Scan in progress.......")

        result = subprocess.check_output(
                ["nmcli", "-t", "-f", "SSID, SIGNAL,SECURITY", "dev", "wifi",],
                text=True
                )

        for ligne in result.splitlines():
            ssid, signal, securite = ligne.split(":")
            print(f" {ssid} | {signal}% | {securite}")

    if user == "2":
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))

        ip = s.getsockname()[0]
        s.close()

        print("My local IP :", ip)

    if user == "clear":
        os.system("clear")

    if user == "exit":
        break

    if user == "3":
        print("0S :", platform.system())
        print("Version :", platform.version())
        print("Machine :", platform.machine())

    if user == "4":
        for connexion in psutil.net_connections():
            print(connexion.laddr, "->", connexion.raddr)

    if user == "5":
        mac =uuid.getnode()

        mac_address = ":".join(
                ["{:02x}".format((mac >> i) & 0xff) for i in range(40, -1, -8)]
                )

        time.sleep(0.5)
        print("MAC :", mac_address)

    if user == "6":
        result = subprocess.check_output(
                ["ip", "link"],
                text=True
                )

        print(result)

    if user == "7":
        ip = "8.8.8.8"
        result = subprocess.run(
                ["ping", "-c", "1", ip],
        )
        print(result.stdout)

    if user == "8":
        time.sleep(0.7)
        print("CPU :", platform.processor())
        print("Cores :", psutil.cpu_count())
        print("CPU Usage :", psutil.cpu_percent(), "%")

        ram = psutil.virtual_memory()

        print("Total RAM :", round(ram.total / (1024**3), 2), "GB")
        print("Used RAM :", round(ram.used / (1024**3), 2), "GB")
        print("RAM Usage :", ram.percent, "%")


    if user == "9":
        result = subprocess.check_output(
                ["lsblk", "-o", "NAME,SIZE,FSTYPE,MOUNTPOINT,MODEL"],
                text=True
        )

        print(result)

    if user == "10":
        try:
            public_ip = urlopen("https://api.ipify.org", timeout=5).read().decode("utf-8")
            print("Public IP:", public_ip)
        except Exception:
            print("Public IP: Unable to retrieve")

