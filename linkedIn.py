import json
import os
import subprocess as subp
import requests

api_url = 'https://api.linkedin.com/v2/me'

url = 'https://www.linkedin.com/oauth/v2/accessToken'

post_url = 'https://api.linkedin.com/v2/ugcPosts'

def get_token():

    with open('config.json', 'r') as f:
        token = json.load(f)
    access_token = token['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json',
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:

        return access_token
    
    elif response.status_code == 401 :
        # params = {
        #     "grant_type": "authorization_code",
        #     "state": "12345",
        #     "code": "AQRxHpEwUKzwfInY7-Pkd5rEepsb66oDfx3XFkJJL1NrGnhw0DZcPGUKKmHwyXHeT38RopxfYr1moQc92K8_Yx6iMrRczSiyhycOedg5mJB1srS7QNofA-WrBMqwouLgl4QDr3c4PA_4ujt8dqDUVfDe8Q7hSqy4YJKW7eNGQh3ze_oUhmBt3h-LauM4bwUfFM7dDpCSeTCt3zwX_ec",
        #     "redirect_uri": "https://richenelai.azurewebsites.net/",
        #     "client_id": "782dfwzsm227fw",
        #     "client_secret": "GnHW1Undlb6F2RiI"
        # }
        response = requests.post(url, headers={
            "Content-Type":"x-www-form-urlencoded"
        },params={
            "grant_type":"refresh_token",
            "refresh_token":token["refresh_token"],
            "client_id": "782dfwzsm227fw",
            "client_secret": "GnHW1Undlb6F2RiI"})
        # response = requests.post(url, params=params)

        if response.status_code == 200:
            access_token = response.json()['access_token']
            with open('config.json', 'w') as json_file:
                token["access_token"]=access_token
                json.dump(token, json_file)
            return access_token
        else:
            print('Error:', response.status_code, response.text)
    print(response.text)
    

def post_linkedin(message,image,access_token=None):
    if access_token == None:
        access_token = get_token()

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    data = {
        "registerUploadRequest": {
            "recipes": [
                "urn:li:digitalmediaRecipe:feedshare-image"
            ],
            "owner": "urn:li:company:101161994",
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }

    register_upload = requests.post('https://api.linkedin.com/v2/assets?action=registerUpload', headers=headers, data=json.dumps(data))
    print(register_upload.text)
    upload_url = register_upload.json()['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest'][
        'uploadUrl']
    asset = register_upload.json()['value']['asset']

    response = requests.put(f'{upload_url}', data=image,headers=headers)   

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json',
    }
    post_body= {
        "author": "urn:li:company:101161994",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": "Center stage!"
                        },
                        "media": f"{asset}",
                        "title": {
                            "text": "LinkedIn Talent Connect 2021"
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    response = requests.post(post_url, headers=headers, json=post_body)
    if response.status_code == 201:
        print('Post successfully created!')
    else:
        print(f'Post creation failed with status code {response.status_code}: {response.text}')

if __name__ == '__main__':
    post_linkedin(message="Hello world")
