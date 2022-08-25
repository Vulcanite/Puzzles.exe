import psutil
import math
import subprocess, json
import re
import subprocess
import json
from .constants import ram_type, manufacturer_names, form_factor
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_config():
    config = dict()
    machine_type = subprocess.getoutput("PowerShell -Command \"& { Get-CimInstance Win32_SystemEnclosure | Select-Object -ExpandProperty ChassisTypes}\"")
    if(int(machine_type) in [3,4,5,6,7,15,16]):
        config["Device-Type"]="Desktop"
    else:
        config["Device-Type"]="Laptop"

    config["Private IP Address:"] = get_ip()

    l=[]
    
    #CPU INFORMATION
    out = subprocess.getoutput("PowerShell -Command \"& {Get-CimInstance -Class CIM_Processor | Select Name,Manufacturer,NumberOfCores,ThreadCount,MaxClockSpeed|ConvertTo-Json}\"")
    j=json.loads(out)
    config["CPU"]={"Name":j["Name"],"ClockSpeed": str(j["MaxClockSpeed"]/1000)+" GHz","Manufacturer":j["Manufacturer"],"No. Of Cores":j["NumberOfCores"],"Thread Count":j["ThreadCount"]}

    #GPU INFORMATION
    try:
        l=[]
        out_gpu=subprocess.getoutput("PowerShell -Command \"& {Get-WmiObject Win32_VideoController| select name,AdapterCompatibility|ConvertTo-Json}\"")
        j=json.loads(out_gpu)

        for i in j:
            l.append({"Model":i["name"],"Vendor":i["AdapterCompatibility"]})

        config["GPU"]=l

    except:
        config["GPU"]=[{"Name":None}]

    #RAM INFORMATION
    l=[]
    out1 = subprocess.getoutput("PowerShell -Command \"& {Get-CimInstance win32_physicalmemory | Select Capacity,Manufacturer,SerialNumber,FormFactor,SMBIOSMemoryType,Speed|ConvertTo-Json}\"")
    j1 = json.loads(out1)
    
    if isinstance(j1, list):
        for i in j1: 
            l.append({"Manufacturer":i["Manufacturer"],"Type":ram_type[str(i["SMBIOSMemoryType"])],"Form Factor": form_factor[str(i["FormFactor"])],"Memory":str(math.ceil( i["Capacity"]/ (1024.0 ** 3)))+ " GB","Speed":str(i["Speed"])+" MHz"})

        config["RAM"]=l
    else:
        config["RAM"]=[{"Manufacturer":j1["Manufacturer"],"Type":ram_type[str(j1["SMBIOSMemoryType"])],"Form Factor": form_factor[str(j1["FormFactor"])],"Memory":str(math.ceil(j1["Capacity"]/ (1024.0 ** 3)))+ " GB","Speed":str(j1["Speed"])+" MHz"}]

    #HDD INFORMATION
    try:
        l=[]
        hdd = psutil.disk_usage('/')
        out2 = subprocess.getoutput("PowerShell -Command \"& {Get-PhysicalDisk| Select Size, SerialNumber, MediaType,Model| ConvertTo-Json}\"")
        j2=json.loads(out2)

        for i in j2:
            if i["MediaType"]=="HDD":
                l.append({"Model":i["Model"],"Serial Number":i["SerialNumber"],"Memory":str(math.ceil((i["Size"]/ (1024.0**3))/1000))+" TB"})
        config["HDD"]=l
    except:
        config["HDD"]={"Model":None,"Serial Number":None,"Memory":None}

    #SSD INFORMATION
    l=[]
    try:
        for i in j2:
            if i["MediaType"]=="SSD":
                ssd=i["Size"]/(1024.0**3)
                if(ssd<128):
                    s="128 GB"
                elif(ssd>128 and ssd<256):
                    s="256 GB"
                elif(ssd>256 and ssd<512):
                    s="512 GB"
                else:
                    s="1 TB"

                l.append({"Model":i["Model"],"Serial Number":i["SerialNumber"],"Memory":s})

        config["SSD"]=l
    except:
        config["SSD"]=[{"Model":None,"Serial Number":None,"Memory":None}]

    #MOTHERBOARD INFORMATION
    out3 = subprocess.getoutput("PowerShell -Command \"& {Get-WmiObject Win32_BaseBoard|Select  Manufacturer,SerialNumber, Product | ConvertTo-Json}\"")
    j3=json.loads(out3)

    if(j3["Product"].isspace()):
        j3["Product"]="None"
    config["Motherboard"]={"Manufacturer":j3["Manufacturer"],"Serial Number":j3["SerialNumber"],"Product":j3["Product"]}

    #MOUSE INFORMATION
    try:
        out4 = subprocess.getoutput("PowerShell -Command \"& {'win32_pointingdevice'| % {gwmi $_ | ? description -match 'hid'} | Select description, PNPDeviceID|ConvertTo-Json}\"")
        j4=json.loads(out4)
        index1=re.search(r'VID_',j4["PNPDeviceID"]).end()
        index2=re.search(r'PID_',j4["PNPDeviceID"]).end()
        config["Mouse"]={"Vendor ID":j4["PNPDeviceID"][index1:index1+4],"Product ID":j4["PNPDeviceID"][index2:index2+4]}
 
    except:
        config["Mouse"]={"Vendor ID":None,"Product ID":None}

    #KEYBOARD INFORMATION
    try:
        out5 = subprocess.getoutput("PowerShell -Command \"& {'win32_keyboard'| % {gwmi $_ | ? description -match 'hid'} | Select description, PNPDeviceID|ConvertTo-Json}\"")
        j5=json.loads(out5)
        index1=re.search(r'VID_',j5["PNPDeviceID"]).end()
        index2=re.search(r'PID_',j5["PNPDeviceID"]).end()
        config["Keyboard"]={"Vendor ID":j5["PNPDeviceID"][index1:index1+4],"Product ID":j5["PNPDeviceID"][index2:index2+4]}

    except:
        config["Keyboard"]={"Vendor ID":None,"Product ID":None}

    l=[]
    try:
        out6 = subprocess.getoutput("PowerShell -Command \"& {gwmi WmiMonitorID -Namespace root\\wmi| Select InstanceName|ConvertTo-JSON}\"")
        j6=json.loads(out6)

        out7 = subprocess.getoutput("PowerShell -Command \"& {Get-WmiObject win32_videocontroller | select CurrentHorizontalResolution, CurrentVerticalResolution,MaxRefreshRate|ConvertTo-JSON}\"")
        j7=json.loads(out7)

        print(j7)

        if len(j6)==1:
            index=re.search(r'\\[A-Z]{3}[A-Za-z0-9]{4}\\',j6["InstanceName"]).start()
            l.append({"Model":j6["InstanceName"][index+1:index+7],"Manufacturer":manufacturer_names[j6["InstanceName"][index+1:index+7][0:3]]})

        else:
            for i in range(len(j6)):
                index=re.search(r'\\[A-Z]{3}[A-Za-z0-9]{4}\\',j6[i]["InstanceName"]).start()

                l.append({"Model":j6[i]["InstanceName"][index+1:index+7],"Manufacturer":manufacturer_names[j6[i]["InstanceName"][index+1:index+7][0:3]]})
        config["Monitor"]=l

    except:
        config["Monitor"]=[{"Model":None,"Manufacturer":None}]
    return config
		
