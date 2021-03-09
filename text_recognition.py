"""
Goal:-
To extract text from an image using
azure read api

Python 3rd Party Modules:-
1. requests module (pip install requests)
"""
import os
import json# to convert json to python dictionary
import time
import requests# to make requests to the api


def send_data(API_KEY,ENDPOINT,IMAGE_PATH):
    """
    Function to send data to 
    Azure read api
    """
    f = open(IMAGE_PATH,'rb')
    data = f.read()
    params   = {
    'language': "en",
    'detectOrientation ': 'true'
    }
    headers = {'Ocp-Apim-Subscription-Key':API_KEY,
    'Content-Type': 'application/octet-stream'}
    post_request = requests.post(ENDPOINT, data=data, headers=headers, params=params)
    print(post_request)
    results = post_request.headers# getting the headers
    get_url = results.get('Operation-Location')
    # time.sleep(.25)# wait until the response is returned
    get_request = requests.get(get_url, headers=headers)
    text = get_request.text
    returned_json = json.loads(text)
    check = returned_json.get("status")
    while check!='succeeded':
        time.sleep(.01)
        print(1)
        get_request = requests.get(get_url,headers=headers)
        returned_json = json.loads(get_request.text)
        check = returned_json.get("status")


    returned_json = get_request.text

    returned_dict = json.loads(returned_json)# converting the json to python dict
    return returned_dict

def parse_json(returned_json):
    """
    Function to parse the json 
    and find the text
    """
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
    ENDPOINT = "{your endpoint}/vision/v3.1/read/analyze"
    API_KEY = "your api key"
    IMAGE_PATH = "/Users/shauryakanda/Desktop/ocr_sample1.png"
    returned_data = send_data(API_KEY,ENDPOINT,IMAGE_PATH)
    parsed_text = parse_json(returned_data)
    print(parsed_text)
