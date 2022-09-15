from fastapi import FastAPI, Request
from flask import Flask, request, jsonify, abort
import requests
import uvicorn
from pydantic import BaseModel
import base64  
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import uuid
app = FastAPI()

#autopep8 outil pour bien indenter son code
#pour tester son api http://127.0.0.1:port/docs#/default/home_end_point_get
#pour faire une belle documentation
#http://127.0.0.1:port/redoc

class File(BaseModel):
    content:str
    password:str

@app.post("/postData/")
async def test_method(file:File):
    # print(request.json)
    #if not request.json or 'file' not in request.json:
    #    abort(400)
    print("File recu cote serveur ")
    file_b64 = file.content
    password=file.password


    # convert it into bytes
    file_bytes = base64.b64decode(file_b64.encode('utf-8'))
    
    #Le fichier output 
    chaine_id=str(uuid.uuid4())
    filename_out="output"+chaine_id+".pdf"
    filename_in="input"+chaine_id+".pdf"

    #Le fichier input 
    file_in=open(filename_in,"wb")
    file_in.write(file_bytes)
    file_in.close()
    
    encrypt_file(filename_in,password,filename_out)
    #file_out.close()

    with open(filename_out,"rb") as f:
        file_out_bytes=f.read()



    result_dict = {'output':base64.b64encode(file_out_bytes).decode("utf-8")}
    os.remove(filename_in)
    os.remove(filename_out)
    return result_dict
#============================================================
def encrypt_file(filename_in,password,filename_out):

    out = PdfFileWriter()
      
    # Open our PDF file with the PdfFileReader
    file = PdfFileReader(filename_in)
    num = file.numPages
    for idx in range(num):
        page = file.getPage(idx)
        out.addPage(page)

    #Encrypt the new file with the entered password
    out.encrypt(password)
      
    # Open a new file "myfile_encrypted.pdf"
    with open(filename_out, "wb") as f:
        out.write(f)
    #filename_out.close()
    
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8080, debug=True)
