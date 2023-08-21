# ip address log
'''
# IPAddress_Log.py
# created by mahemys; 2021.04.04
# !perfect, but works!
# GNU-GPL; no license; free to use!
# update 2021-04-04; initial review
#
#------------------------------------------------------------
# ipinfo.io       - refer documentation for latest info.
# Free-Plan       - https://ipinfo.io/developers/responses#free-plan
# MissingAuth     - https://ipinfo.io/missingauth
# Unauthenticated - Request limit increase from 1k/day to 50k/month.
# Rate Limits     - Free usage is limited upto 50,000 API requests per month.
# request         - https://ipinfo.io/{ip}/{field}/
# field           - ip, hostname, anycast, city, region, country, loc, org, postal, timezone, readme
#------------------------------------------------------------
'''
import os
import requests
from datetime import datetime

ip  = None
LOG = 'ip_public.txt'
URL = 'https://ipinfo.io/ip'

time_start = datetime.now()
print('Start  {}'.format(time_start))

try:
    #get ip address
    r = requests.get(URL, timeout=3.00)
    if r.status_code == 200:
        ip = r.content.decode('ascii').rstrip('\n')
        
        print("Status {} {} {}".format(datetime.now(), r.status_code, ip))
    else:
        print("Error  {} {} {}".format(datetime.now(), r.status_code, ip))
except:
    print('#Exception: get ip', ip)
    pass

try:
    #read last ip from log
    if os.path.exists(LOG):
        f_file = open(LOG, 'r')
        f_line = f_file.readlines()
        f_file.close()
        
        t_line = len(f_line)
        print("Found  {} {} {}".format(datetime.now(), LOG, t_line))
    else:
        t_line = 0
        print("NoFile {} {} {}".format(datetime.now(), LOG, t_line))
    
    if t_line == 0:
        last_date = datetime.now().strftime('%Y-%m-%d')
        last_time = datetime.now().strftime('%H:%M:%S.%f')
        last_ip   = None
    else:
        #last_ip  = f.readlines()[-1].split()[-1]
        last_line = f_line[-1]
        last_date = last_line.split()[-3]
        last_time = last_line.split()[-2]
        last_ip   = last_line.split()[-1]
    
    time_last = last_date + " " + last_time
except:
    print('#Exception: read log', LOG)
    pass

try:
    #save new ip to log
    if ip == None:
        print("ip err {} {}".format(datetime.now(), ip))
    elif ip != last_ip:
        f_file = open(LOG, 'a')
        f_file.write("{}\t{}\n".format(datetime.now(), ip))
        f_file.close()
        print("ip new {} {}".format(datetime.now(), ip))
    else:
        print("ip old {} {}".format(datetime.now(), ip))
except:
    print('#Exception: write log', LOG)
    pass

#calculate time difference
dtfmt = '%Y-%m-%d %H:%M:%S.%f'
time1 = str(time_start)#'2020-05-12 16:09:37.0'
time2 = str(time_last) #'2020-05-13 11:35:34.0'

tstamp1 = datetime.strptime(time1, dtfmt)
tstamp2 = datetime.strptime(time2, dtfmt)

if tstamp1 > tstamp2:
    td = tstamp1 - tstamp2
else:
    td = tstamp2 - tstamp1
td_mins = int(round(td.total_seconds() / 60))
print('Diff   {}\t{}m\t{}s'.format(td, td_mins, td.total_seconds()))

time_stop = datetime.now()
time_diff = time_stop-time_start
print('ExTime {}'.format(time_diff))
