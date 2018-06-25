#otx_feed.py
import requests 
import json
import re
import datetime
import sys
api_key=""

if len(api_key.strip())<1:
	print("No api key specified.")
	sys.exit(1)
now=datetime.datetime.utcnow()
yesterday=datetime.datetime(now.year,now.month,now.day-1,now.hour,now.minute,now.second,now.microsecond).isoformat()

response=requests.get("https://otx.alienvault.com/api/v1/indicators/export?limit=5000&modified_since="+yesterday.strip(),headers={"X-OTX-API-KEY":api_key})
#print(response.text)
jdata=json.loads(response.text)
ioclist={"domain":[],"ipv4":[],"md5":[],"sha256":[]}
if "results" in jdata:
	output=""
	for r in jdata["results"]:
		if "indicator" in r:
			if "type" in r:
				description=""
				if "description" in r:
					description=r["description"]
				if r["type"] in ["domain","hostname"]:
					ioclist["domain"].append([r["indicator"].strip(),description])
				elif r["type"].lower().strip() == "filehash-md5":
					ioclist["md5"].append([r["indicator"],description])
				elif r["type"].lower().strip() == "filehash-sha256":
					ioclist["sha256"].append([r["indicator"],description])
				elif r["type"].lower().strip() == "ipv4":
					ioclist["ipv4"].append([r["indicator"],description])
				elif r["type"].lower().strip() == "url":
					m=re.match(r"https?://([\w\d\.\-]*)[\:/]+.*",r["indicator"])
					if not None is m and not None is m.group(1):
						m2=re.match("\d+\.\d+\.\d+\.\d+",m.group(1))
						if not None is m2:
							ioclist["ipv4"].append([m.group(1),description])
						else:
							ioclist["domain"].append([m.group(1),description])
filename="ioclist.csv"
if len(sys.argv)>1 and len(sys.argv[1])>1:
	filename=sys.argv[1]
with open(filename,"w+") as iocfile:				
	print("IOC Type\tIndicator\tDescription")
	iocfile.write("IOC Type,Indicator,Description\n")
	for k in ioclist:
		#print(("*"*50)+k+("*"*50))
		for e in ioclist[k]:
			desc="\n"
			odesc=""
			if len(e[1].strip())<1:
				desc=",\n"
				odesc=" <no description>"
			else:
				desc=e[1]
			print k+"\t"+e[0]+"\t"+odesc
			iocfile.write(k+","+e[0]+","+desc)
print("ioc list written to "+filename)