"""
Goal:-
To extract text from an image using
azure read api
Python 3rd Party Modules:-
1. requests module (pip install requests)
"""

import json
import time
import requests
ENDPOINT = "{endpoint}/vision/v3.1/read/analyze"
IMAGE_PATH = "/Users/shaurya/Desktop/Archive/Aadhar1.png"
API_KEY = "you api key"

def send_data(API_KEY,ENDPOINT,IMAGE_PATH):
    f = open(IMAGE_PATH,'rb')
    data = f.read()
    params   = {
                    'language': "en",
                    'detectOrientation ': 'true'
                }

    headers = {'Ocp-Apim-Subscription-Key':API_KEY,

    'Content-Type': 'application/octet-stream'}
    r = requests.post(ENDPOINT,data=data,headers = headers,params = params)
    str_post = str(r)
    results = r.headers
    get_url = results.get('Operation-Location')

    time.sleep(.50)# read api takes some time to return the response
    get_requests = requests.get(get_url,headers=headers)
    text = get_requests.text
    returned_json = json.loads(text)
    return returned_json

def parse_json(returned_json):
    parsed_text = ""
    analyzed_res = returned_json.get("analyzeResult")
    read_res = analyzed_res.get("readResults")
    read_res = read_res[0]
    lines = read_res.get("lines")
    for line in lines:
        text = line.get("text")
        parsed_text += f"{text}\n"
    return parsed_text

if __name__=="__main__":
    returned_data = send_data(API_KEY,ENDPOINT,IMAGE_PATH)
    extracted_text = parse_json(returned_data)
    print(extracted_text)

