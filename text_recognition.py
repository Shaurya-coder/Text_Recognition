"""
Goal:-
To extract text from an image using
azure read api

Python 3rd Party Modules:-
1. requests module (pip install requests)
"""

import json# to convert json to python dictionary
import time
import requests# to make requests to the api
ENDPOINT = "{your endpoint}/vision/v3.1/read/analyze"
API_KEY = "your api key"
IMAGE_PATH = "ocr_sample.png"

def send_data(API_KEY,ENDPOINT,IMAGE_PATH):
    f = open(IMAGE_PATH,'rb')
    data = f.read()
    params   = {
    'language': "en",
    'detectOrientation ': 'true'
    }
    headers = {'Ocp-Apim-Subscription-Key':API_KEY,
    'Content-Type': 'application/octet-stream'}
    post_request = requests.post(ENDPOINT, data=data, headers = headers, params = params)
    results = post_request.headers# getting the headers

    get_url = results.get('Operation-Location')
    time.sleep(.50)# wait until the response is returned
    get_request = requests.get(get_url, headers=headers)

    returned_json = get_request.text

    returned_dict = json.loads(returned_json)# converting the json to python dict
    return returned_dict



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
