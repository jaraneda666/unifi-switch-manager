import urllib3
import requests
import json
import time

urllib3.disable_warnings()

s = requests.Session()
s.verify = False

payload = {
    'username': os.environ.get("ADMIN_USER", "admin"),
    'password': os.environ.get("ADMIN_PASS", ""),
    'ubic_2fa_token': '000000',
    'remember': True,
    'strict': True
}

try:
    login_res = s.post('https://192.168.1.100:8443/api/login', json=payload, timeout=5)
    print(f'Login HTTP status: {login_res.status_code}')
    if login_res.status_code != 200:
        print('Login response:', login_res.text)
        exit(1)

    r = s.get('https://192.168.1.100:8443/api/s/default/stat/device', timeout=5)
    if r.status_code == 200:
        devs = r.json().get('data', [])
        print(f'Total devices: {len(devs)}')
        for d in devs:
            name = d.get('name') or 'Sin nombre'
            model = d.get('model')
            mac = d.get('mac')
            ip = d.get('ip')
            state = d.get('state')
            adopted = d.get('adopted')
            uptime = d.get('uptime')
            last_seen = d.get('last_seen')
            now = time.time()
            ago = int(now - last_seen) if last_seen else 'N/A'
            print(f"- {name} ({model}) | MAC: {mac} | IP: {ip} | State: {state} | Adopted: {adopted} | Last seen: {ago}s ago")
            if model == 'US8P60' or mac == 'e0:63:da:27:66:82':
                print(f"  Switch detail: state={state}, adopting={d.get('adopting')}, adopted={adopted}, ip={ip}, mgmt_network_id={d.get('mgmt_network_id')}")
    else:
        print('Error querying devices:', r.status_code, r.text)

    # Check pending adoption or discovered devices
    r_discovered = s.get('https://192.168.1.100:8443/api/s/default/stat/device-basic', timeout=5)
    if r_discovered.status_code == 200:
        d_data = r_discovered.json().get('data', [])
        print(f"Basic devices count: {len(d_data)}")

except Exception as ex:
    print(f'Error: {ex}')
