import paramiko
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

SWITCH_IP = "192.168.1.252"
USER = "ubnt"
PASS = "ubnt"

print(f"1. Conectando al Switch UniFi US-8-60W ({SWITCH_IP})...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SWITCH_IP, port=22, username=USER, password=PASS, timeout=5, look_for_keys=False, allow_agent=False)
chan = ssh.invoke_shell()
time.sleep(1)

def send_cmd(cmd, wait=0.5):
    chan.send(cmd + "\n")
    time.sleep(wait)

send_cmd("telnet 127.0.0.1 23")
send_cmd("enable")

print("2. Creando VLANs 60 y 70 en la base de datos de VLAN...")
send_cmd("vlan database")
send_cmd("vlan 60,70")
send_cmd("vlan name 60 IOT")
send_cmd("vlan name 70 GUEST")
send_cmd("exit")

print("3. Configurando enlaces troncales (tagging 60,70) en interfaces 0/1, 0/6 y 0/8...")
send_cmd("configure")

# Puerto 0/1 (Uplink a Router ASUS RT-AC88U lan1)
send_cmd("interface 0/1")
send_cmd("vlan participation include 60,70")
send_cmd("vlan tagging 60,70")
send_cmd("exit")

# Puerto 0/6 (Downlink a AP2)
send_cmd("interface 0/6")
send_cmd("vlan participation include 60,70")
send_cmd("vlan tagging 60,70")
send_cmd("exit")

# Puerto 0/8 (Downlink a AP1)
send_cmd("interface 0/8")
send_cmd("vlan participation include 60,70")
send_cmd("vlan tagging 60,70")
send_cmd("exit")

send_cmd("exit")

print("4. Guardando configuración en memoria persistente (write memory)...")
send_cmd("write memory", wait=2)
# Por si requiere confirmación 'y'
send_cmd("y", wait=1)

print("5. Verificando estado de VLANs...")
send_cmd("terminal length 0")
send_cmd("show vlan")
time.sleep(1)

out = chan.recv(65535).decode("utf-8", errors="replace")
print("=== SALIDA FASTPATH ===")
print(out)

ssh.close()
