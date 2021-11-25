import re
import subprocess
from influxdb import InfluxDBClient

ip = subprocess.Popen("host myip.opendns.com resolver1.opendns.com | grep \"myip.opendns.com has\" | awk '{print $4}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

ip = ip.replace("\n","")

client = InfluxDBClient('localhost', 8086, 'monitor', 'picapapas', 'monitor')

client.write_points([
	{
		"measurement": "public_ips",
		"tags": {
			"host": "ip"
		},
		"fields": {
			"current": ip
		}
	}
])

cpu = subprocess.Popen("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage \"%\"}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
ram = subprocess.Popen("free -m | grep Mem | awk '{print $3}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
swap = subprocess.Popen("free -m | grep Swap | awk '{print $3}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

ram_percent = subprocess.Popen("free -m | grep Mem | awk '{print ($3/$2)*100}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
swap_percent = subprocess.Popen("free -m | grep Swap | awk '{print ($3/$2)*100}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

cpu = float(cpu.replace('%',''))
ram = float(ram)
swap = float(swap)
ram_percent = float(ram_percent)
swap_percent = float(swap_percent)

client.write_points([
    {
        "measurement" : "performance",
        "tags" : {
            "host": "raspberry"
        },
        "fields" : {
            "cpu": cpu,
            "ram": ram,
            "swap": swap,
	    "ram_percent": ram_percent,
            "swap_percent": swap_percent
        }
    }
])
