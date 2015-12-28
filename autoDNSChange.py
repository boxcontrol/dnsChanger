import os
import winreg
import admin
if not admin.isUserAdmin():
        admin.runAsAdmin()


print(os.popen('ipconfig /all').read())

googleDns = '8.8.4.4 8.8.8.8'
openDns = '208.67.222.222 208.67.220.220'
level3Dns = '209.244.0.3 209.244.0.4'
comodoSecureDNS = '8.26.56.26 8.20.247.20'
nortonSafeDns = '199.85.126.10 199.85.127.10'
yandexDns = '77.88.8.8 77.88.8.1'
heDns = '74.82.42.42'


a = input("Enter DNS servers to use:\n"
          "1 for Google\n"
          "2 for Open DNS\n"
          "3 for Level3\n"
          "4 for Comodo Secure\n"
          "5 for Norton ConnectSafe\n"
          "6 for Yandex\n"
          "7 for Hurricane Electric\n"
          ">>")
DNS_setup = googleDns
if a == '1':
    DNS_setup = googleDns
elif a == '2':
    DNS_setup = openDns
elif a == '3':
    DNS_setup = level3Dns
elif a == '4':
    DNS_setup = comodoSecureDNS
elif a == '5':
    DNS_setup = nortonSafeDns
elif a == '6':
    DNS_setup = yandexDns
elif a == '7':
    DNS_setup = heDns
else:
    a = input("Enter DNS servers to use:(1 for google's DNS; 2 for openDNS.\n>>")


regKey1 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                         'SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\',
                         0, winreg.KEY_ALL_ACCESS)
keyList = []
try:
    i = 0
    while True:
        subkey = winreg.EnumKey(regKey1, i)
        keyList.append(subkey)
        i += 1
except WindowsError:
    pass

keyToChange = ''
for i in keyList:
    regKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            'SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\'+i,
                            0, winreg.KEY_ALL_ACCESS)
    try:
        value, type = winreg.QueryValueEx(regKey, 'DhcpNameServer')
        keyToChange = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                     'SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\' + i,
                                     0, winreg.KEY_ALL_ACCESS)
        print(value)
        if value != DNS_setup:
            try:
                winreg.SetValueEx(keyToChange, 'DhcpNameServer', 0, winreg.REG_SZ, DNS_setup)
                winreg.CloseKey(keyToChange)
                print(regKey1, ', changed to ', DNS_setup, 'servers')
            except WindowsError:
                pass

    except FileNotFoundError:
        pass

print(os.popen('ipconfig /flushdns').read())

input_exit = input('Press ENTER to exit ...')
if input_exit != '':
    raise SystemExit
else:
    pass