"""
# Tool: configure_switch_trunk.py

## Metadata
- Nombre: configure_switch_trunk.py
- Versión: 1.0
- Lenguaje: Python
- Creada en proyecto: OpenWrt_Manager
- Fecha de creación: 2026-10-06
- Descripción: Configura VLANs 60 y 70 en el switch UniFi US-8-60W y define el Puerto 3 como Trunk.
- Parámetros: --host, --user, --password
- Dependencias: paramiko
"""

import argparse
import time
import sys
from pathlib import Path

try:
    import paramiko
except ImportError:
    paramiko = None


def send_and_wait(chan, cmd, delay=0.5):
    chan.send(cmd + "\n")
    time.sleep(delay)


def main():
    parser = argparse.ArgumentParser(description="Configuración Trunk Switch UniFi")
    parser.add_argument("--host", default="192.168.1.1003", help="IP del switch")
    parser.add_argument("--user", default="ubnt", help="Usuario SSH")
    parser.add_argument("--password", default="ubnt", help="Contraseña")

    args = parser.parse_args()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(args.host, port=22, username=args.user, password=args.password, timeout=5, look_for_keys=False, allow_agent=False)

    chan = ssh.invoke_shell()
    time.sleep(1)

    commands = [
        "telnet 127.0.0.1 23",
        "enable",
        "vlan database",
        "vlan 60,70",
        "vlan name 60 IOT",
        "vlan name 70 GUEST",
        "exit",
        "configure",
        "interface 0/3",
        "vlan participation include 60,70",
        "vlan tagging 60,70",
        "exit",
        "exit",
        "terminal length 0",
        "show vlan",
        "show running-config interface 0/3",
    ]

    for c in commands:
        send_and_wait(chan, c, delay=0.6)

    time.sleep(2)
    output = ""
    while chan.recv_ready():
        output += chan.recv(8192).decode("utf-8", errors="replace")
        time.sleep(0.3)

    print("=== RESULTADO CONFIGURACIÓN FASTPATH ===")
    print(output)

    chan.close()
    ssh.close()


if __name__ == "__main__":
    main()
