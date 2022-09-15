import base64
import json 
import requests
api='http://localhost:8080/postData/'
file='file.pdf'

with open(file,"rb") as f:
	file_bytes=f.read()

file_b64=base64.b64encode(file_bytes).decode("utf-8")
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  
payload = json.dumps({"content": file_b64,"password":"123"})



response = requests.post(api,data=payload,headers=headers)
try:
    data = response.json()     
    file_b64=data['output'] 
    file_bytes = base64.b64decode(file_b64.encode('utf-8'))  

    file_encrypted=open("encrypted.pdf","wb")
    file_encrypted.write(file_bytes)
    file_encrypted.close()             
except requests.exceptions.RequestException:
    print(response.text)