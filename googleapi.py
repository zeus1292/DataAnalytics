import json
import requests
import string
import random

def get_businesses(query,api_key,min_rating=0.0,max_results=30):
    answer_list=list()
    try:
        if int(min_rating):
            None
    except:
        print("min_rating is in incorrect format")
        return answer_list
    try:
        if int(max_results):
            None
    except:
        print("max_results is in incorrect format")
        return answer_list
        
    base_url="https://maps.googleapis.com/maps/api/place/textsearch/json?"
    url=""
    query=query.replace(' ','+')
    url+=base_url+"query="+query+'&key='+api_key
    
    try:
        response=requests.get(url)
    except:
        print("Something went wrong with the API call",response.status_code)
        return
    
    try:
        data_string=response.content.decode('utf-8')
    except:
        print("There is a problem with the decoding")
        return
    
    python_data=json.loads(data_string)
    adding_list_values(answer_list,python_data,min_rating,max_results)
    if(len(answer_list)>=max_results):
        return answer_list
    while 'next_page_token' in python_data.keys():
        if(len(answer_list)>=max_results):
            break
        url=base_url+"pagetoken="+python_data['next_page_token']+"&key="+api_key
        response=requests.get(url)
        while response.json().get('status')!='OK':
            from time import sleep
            from random import random
            sleep(random())
            response=requests.get(url)
        try:
            data_string=response.content.decode('utf-8')
        except:
            print("There is a problem with the decoding")
            return
        python_data=json.loads(data_string)
        adding_list_values(answer_list,python_data,min_rating,max_results)
        
    return answer_list

def adding_list_values(answer_list,p_data,min_rating,max_results):
    for i in p_data['results']:
        flist=[]
        if len(answer_list)>=max_results:
            break
        if i['rating']<=min_rating:
            continue
        flist.append(i.get('name'))
        flist.append(i.get('formatted_address'))
        flist.append(i.get('opening_hours'))
        flist.append(i.get('price_level'))
        flist.append(i.get('rating'))
        answer_list.append(tuple(flist))
        
#API KEY
# You'll need an API key to make a request to the Google API.
key = "" 

# #Query string and test cases
# gl_pdata=get_businesses("restaurants near Columbia University",key,4.5,45)
# print(gl_pdata)
# print(len(gl_pdata))
# gl_pdata=get_businesses("restaurants near Columbia University",key,max_results=70)
# print(gl_pdata)
# print(len(gl_pdata))
# gl_pdata=get_businesses("restaurants near Columbia University",key)
# print(gl_pdata)
# print(len(gl_pdata))
# gl_pdata=get_businesses("restaurants near Columbia University",key,min_rating=None, max_results = 20)
# print(gl_pdata)
# print(len(gl_pdata))
# gl_pdata=get_businesses("restaurants near Columbia University",key, max_results = None)
# print(gl_pdata)
# print(len(gl_pdata))
# gl_pdata=get_businesses("restaurants near Columbia University",key,min_rating=3.0, max_results = 30)
# print(gl_pdata)
# print(len(gl_pdata))
# gl_pdata=get_businesses("restaurants near Columbia University",key,min_rating=4.6, max_results = 50)
# print(gl_pdata)
# print(len(gl_pdata))
# gl_pdata=get_businesses("restaurants near Columbia University",key, max_results = 20)
# print(gl_pdata)
# print(len(gl_pdata))
# gl_pdata=get_businesses("restaurants near Columbia University",key,min_rating=4.0)
# print(gl_pdata)
# print(len(gl_pdata))
# gl_pdata=get_businesses("restaurants near Columbia University",key,max_results='a')
# print(gl_pdata)
# print(len(gl_pdata))
# gl_pdata=get_businesses("restaurants near Columbia University",key,min_rating='b')
# print(gl_pdata)
# print(len(gl_pdata))
