from urllib.request import urlopen
from rich import print
import time
import os
import subprocess
import socket
import platform
import psutil
import uuid
import shutil

os.system("clear")
time.sleep(1)

print('[red]Project SystemEye :[/red]')
time.sleep(0.5)
print(" ")
print("\n [cyan]TOOLS[/cyan]")
print("[cyan]--------[/cyan]")
print("""[cyan]
[1]Wifi scan          [11]Security
[2]Local IP           [12]Packages manager
[3]System infos       [13]Battery infos
[4]Wifi infos         [14]DNS lookup
[5]MAC address        [15]Traceroute
[6]Wifi addr          [16]Reverse DNS lookup
[7]Ping               [17]Port checker
[8]Hardware infos")
[9]Disk infos")
[10]Public IP
[/cyan]""")
print(" ")
print("[cyan]Useful tools: clear exit[/cyan]")
print(" ")

while True:
    user = input("Choose an option: ").strip().lower()
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

    if user == "11":
        print("\n Security")
        print("-----------")

        if os.getuid() == 0:
            print("Root privileges : Yes")
        else:
            print("Root privileges : No")

        try:
            ports = subprocess.check_output(["ss", "-tuln"], text=True)
            print("Open ports    :", len(ports.splitlines()) - 1)
        except:
            print("Open ports    : Error")

        try:
            ssh = subprocess.check_output(
                ["systemctl", "is-active", "sshd"],
                text=True
            ).strip()
            print("SSH Service    :", ssh)
        except:
            print("SSH Service    : Unknow")

        try:
            firewall = subprocess.check_output(
                ["ufw", "status"],
                text=True
            )
            if "active" in firewall.lower():
                print("Firewall    : Active")
            else:
                print("Firewall    : Inactive")
        except:
            print("Firewall    : Not installed")

    if user == "12":
        print("\n Package manager")
        print("------------------")

        if shutil.which("pacman"):
            print("Manager: pacman")
            package = subprocess.check_output(["pacman", "-Q"], text=True)
            print("Installed packages:", len(package.splitlines()))

        elif shutil.which("apt"):
            print("Manager: apt")
            package = subprocess.check_output(
                "dpkg -1 | grep '^ii' | wc -L",
                shell=True,
                text=True
            )
            print("Installed packages:", package.strip())

        elif shutil.which("dnf"):
            print("Manager: dnf")
            package = subprocess.check_output(
                ["dnf", "list", "installed"],
                text=True
            )
            print("Installed packages:", len(package.splitlines()) - 1)

        elif shutil.which("zypper"):
            print("Manager: zypper")
            package = subprocess.check_output(
                ["rpm", "-qa"],
                text=True
            )
            print("Installed packages", len(package.splitlines()))

        elif shutil.which("apk"):
            print("Manager: apk")
            package = subprocess.check_output(
                ["apk", "info"],
                text=True
            )
            print("Installed packages", len(package.splitlines()))

        else:
            print("Package Manager: Unknown")

    if user == "13":
        battery = psutil.sensors_battery()

        print("\n Battery")
        print("----------")

        if battery:
            print("Battery level :", battery.percent, "%")

            if battery.power_plugged:
                print("Status    : Charging")
            else:
                print("Status    : Discharging")

            if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                minutes = battery.secsleft // 60
                print("Time left    :", minutes, "minutes")

        else:
            print("Battery    : Not available")

    if user == "14":
        domain = input("Domaine: ")

        try:
            results = socket.getaddrinfo(domain, None)

            print("\nIP Addresses:")
            seen = set()

            for result in results:
                ip = result[4][0]
                if ip not in seen:
                    seen.add(ip)
                    print("-", ip)

        except socket.gaierror:
            print("Unable to resolve domain")

    if user == "15":
        host = input("Host:  ")

        if shutil.which("traceroute"):
            subprocess.run(["traceroute", host])
        elif shutil.which("tracepath"):
            subprocess.run(["tracepath", host])

        else:
            print("Traceroute is not installed.")

    if user == "16":
        ip = input("IP Address:  ")

        try:
            hostname = socket.gethostbyaddr(ip)
            print("Hostname:", hostname[0])
        except socket.herror:
            print("No hostname found !")
        except socket.gaierror:
            print("Invalid IP address")

    if user == "17":
        host = input("Host:  ")
        port = int(input("Port:  "))

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)

        result = sock.connect_ex((host, port))

        if result == 0:
            print(f"Port {port} is OPEN")
        else:
            print(f"Port {port} is CLOSED")

        sock.close()

    