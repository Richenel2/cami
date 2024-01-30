
import json
import requests
# import facebook
def post_facebook(message:str,image_url:str):
    with open('config.json', 'r') as f:
        token = json.load(f)
    access_token = token["facebook"]['access_token']

    # graph = facebook.GraphAPI(access_token=access_token, version="3.1")
    # graph.put_photo(image=open('images/AI Sustainable Futures.jpg', 'rb'),
    #                 message='Look at this cool photo!')
    base_url="https://graph.facebook.com/v19.0/"

    res = requests.post(url=f"{base_url}110962351836360/photos", params={
        "message":message,
        "access_token":access_token,
        "url":image_url,
        "published":True
    })
    print(res.content)

