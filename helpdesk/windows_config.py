from urllib.error import URLError
import psutil
import math
import subprocess, json
import re
import subprocess
import json
import socket
import requests
import json

manufacturer_names={"ACI":"Asus (ASUSTeK Computer Inc.)",
"ACR":"Acer America Corp.",
"ACT":"Targa",
"ADI":"ADI Corporation",
"AMW":"AMW",
"AOC":"AOC International (USA) Ltd.",
"API":"Acer America Corp.",
"APP":"Apple Computer, Inc.",
"ART":"ArtMedia",
"AST":"AST Research",
"AUO":"AU Optronics",
"BMM":"BMM",
"BNQ":"BenQ Corporation",
"BOE":"BOE Display Technology",
"CPL":"Compal Electronics, Inc. / ALFA",
"CPQ":"COMPAQ Computer Corp.",
"CTX":"CTX - Chuntex Electronic Co.",
"DEC":"Digital Equipment Corporation",
"DEL":"Dell Computer Corp.",
"DPC":"Delta Electronics, Inc.",
"DWE":"Daewoo Telecom Ltd",
"ECS":"ELITEGROUP Computer Systems",
"EIZ":"EIZO",
"EPI":"Envision Peripherals, Inc.",
"FCM":"Funai Electric Company of Taiwan",
"FUS":"Fujitsu Siemens",
"GSM":"LG Electronics Inc. (GoldStar Technology, Inc.)",
"GWY":"Gateway 2000",
"HEI":"Hyundai Electronics Industries Co., Ltd.",
"HIQ":"Hyundai ImageQuest",
"HIT":"Hitachi",
"HSD":"Hannspree Inc",
"HSL":"Hansol Electronics",
"HTC":"Hitachi Ltd. / Nissei Sangyo America Ltd.",
"HWP":"Hewlett Packard (HP)",
"HPN":"Hewlett Packard (HP)",
"IBM":"IBM PC Company",
"ICL":"Fujitsu ICL",
"IFS":"InFocus",
"IQT":"Hyundai",
"IVM":"Idek Iiyama North America, Inc.",
"KDS":"KDS USA",
"KFC":"KFC Computek",
"LEN":"Lenovo",
"LGD":"LG Display",
"LKM":"ADLAS / AZALEA",
"LNK":"LINK Technologies, Inc.",
"LPL":"LG Philips",
"LTN":"Lite-On",
"MAG":"MAG InnoVision",
"MAX":"Maxdata Computer GmbH",
"MEI":"Panasonic Comm. & Systems Co.",
"MEL":"Mitsubishi Electronics",
"MIR":"miro Computer Products AG",
"MTC":"MITAC",
"NAN":"NANAO",
"NEC":"NEC Technologies, Inc.",
"NOK":"Nokia",
"NVD":"Nvidia",
"OQI":"OPTIQUEST",
"PBN":"Packard Bell",
"PCK":"Daewoo",
"PDC":"Polaroid",
"PGS":"Princeton Graphic Systems",
"PHL":"Philips Consumer Electronics Co.",
"PRT":"Princeton",
"REL":"Relisys",
"SAM":"Samsung",
"SEC":"Seiko Epson Corporation",
"SMC":"Samtron",
"SMI":"Smile",
"SNI":"Siemens Nixdorf",
"SNY":"Sony Corporation",
"SPT":"Sceptre",
"SRC":"Shamrock Technology",
"STN":"Samtron",
"STP":"Sceptre",
"TAT":"Tatung Co. of America, Inc.",
"TRL":"Royal Information Company",
"TSB":"Toshiba, Inc.",
"UNM":"Unisys Corporation",
"VSC":"ViewSonic Corporation",
"WTC":"Wen Technology",
"ZCM":"Zenith Data Systems"}

ram_type={
	"20": "DDR",
	"21":"DDR2",
	"22":"DDR2 FB-DIMM",
	"24":"DDR3",
	"26":"DDR4"
}

form_factor={
"0":"Unknown",
"1":"Other",
"2":"SIP",
"3":"DIP",
"4":"ZIP",
"5":"SOJ",
"6":"Proprietary",
"7":"SIMM",
"8":"DIMM",
"9":"TSOP",
"10":"PGA",
"11":"RIMM",
"12":"SODIMM",
"13":"SRIMM",
"14":"SMD",
"15":"SSMP",
"16":"QFP",
"17":"TQFP",
"18":"SOIC",
"19":"LCC",
"20":"PLCC",
"21":"DDR2",
"22":"FPBGA",
"23":"LGA"
}

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
        config["DeviceType"]="Desktop"
    else:
        config["DeviceType"]="Laptop"

    config["IPAddress"] = get_ip()

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

        print(j2)

        if type(j2)!=list:
            if j2["MediaType"]=="HDD":
                l.append({"Model":j2["Model"],"Serial Number":j2["SerialNumber"],"Memory":str(math.ceil((j2["Size"]/ (1024.0**3))/1000))+" TB"})
        else:
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
        out4 = subprocess.getoutput("PowerShell -Command \"& {Get-WmiObject win32_PointingDevice|Select PNPDeviceID|ConvertTo-Json}\"")
        j4=json.loads(out4)
        if(type(j4) is list):
           
            l=[]
            for i in j4:
                l.append({"PNPDeviceID":i["PNPDeviceID"]})
        
            config["Mouse"]=l
        else:
            config["Mouse"]={"PNPDeviceID":j4["PNPDeviceID"]}

 
    except:
        config["Mouse"]={"Vendor ID":None,"Product ID":None}

    #KEYBOARD INFORMATION
    try:
        out5 = subprocess.getoutput("PowerShell -Command \"& { Get-CimInstance -ClassName Win32_Keyboard | select PNPDeviceId|ConvertTo-Json}\"")
        j5=json.loads(out5)
        if(type(j5) is list):
            print("in here keyboard")
            l=[]
            for i in j5:
                l.append({"PNPDeviceID":i["PNPDeviceId"]})
            config["Keyboard"]=l
        else:
            config["Keyboard"]={"PNPDeviceID":j5["PNPDeviceId"]}

       

    except:

        config["Keyboard"]={"Vendor ID":None,"Product ID":None}

    l=[]
    try:
        out6 = subprocess.getoutput("PowerShell -Command \"& {gwmi WmiMonitorID -Namespace root\\wmi| Select InstanceName|ConvertTo-JSON}\"")
        j6=json.loads(out6)

        out7 = subprocess.getoutput("PowerShell -Command \"& {Get-WmiObject win32_videocontroller | select CurrentHorizontalResolution, CurrentVerticalResolution,MaxRefreshRate|ConvertTo-JSON}\"")
        j7=json.loads(out7)

        new=[]

        if type(j6)!=list and type(j7)!=list:
            l.append({"Model":j6["InstanceName"],"Resolution": str(j7["CurrentVerticalResolution"])+" x "+str(j7["CurrentHorizontalResolution"]),"MaxRefreshRate":str(j7["MaxRefreshRate"])})
        elif type(j6)!=list and type(j7)==list:
            for i in j7:
                if i["CurrentHorizontalResolution"]==None or i["CurrentVerticalResolution"]==None or i["MaxRefreshRate"]==None:
                    continue
                else:
                    new.append(i)

            l.append({"Model":j6["InstanceName"],"Resolution": str(new[0]["CurrentVerticalResolution"])+" x "+str(new[0]["CurrentHorizontalResolution"]),"MaxRefreshRate":str(new[0]["MaxRefreshRate"])})

        else:
 
            for i in j7:
                if i["CurrentHorizontalResolution"]==None or i["CurrentVerticalResolution"]==None or i["MaxRefreshRate"]==None:
                    continue
            else:
                new.append(i)

            for i in range(len(j6)):
                l.append({"Model":j6[i]["InstanceName"],"Resolution": str(new[0]["CurrentVerticalResolution"])+" x "+str(new[0]["CurrentHorizontalResolution"]),"MaxRefreshRate":str(new[0]["MaxRefreshRate"])})
        config["Monitor"]=l

    except:
        config["Monitor"]=[{"Model":None,"Manufacturer":None}]
    
   

   #CAMERA INFORMATION

    try:
        out8 = subprocess.getoutput("PowerShell -Command \"& { Get-WmiObject Win32_PnPEntity | where {$_.caption -match 'camera'}|Select caption, DeviceID|ConvertTo-Json}\"")
        
        print("before j8")
        j8=json.loads(out8)

        if(type(j8) is list):
            l=[]
            for i in j8:
                l.append({"Name":i["caption"],"Id":i["DeviceID"]})
            config["Camera"]=l
        else:
            config["Camera"]={"Name":j8["caption"],"Id":j8["DeviceID"]}
    except:
            config["Camera"]=[{"Name":None,"Id":None}]

    return config



d=get_config()
# print(d)
API = "http://192.168.168.206:8000/api/getData/"
r = requests.post(url = API, data=json.dumps(d), headers={"content-type":"application/json"})
print(r.text)