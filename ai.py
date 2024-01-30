from openai import OpenAI
import autogen
from linkedIn import post_linkedin
from facebookapi import post_facebook
from typing_extensions import Annotated
import json
from urllib.parse import unquote
import requests
def execute():
    config_list = autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={
            "model": ["gpt-4-1106-preview"],
        },
    )

    llm_config = {
        "config_list": config_list,
        "timeout": 120,
        "cache_seed":None
    }
    chatbot = autogen.AssistantAgent(
        name="chatbot",
        system_message="""Your name is Cami AI and you're an expert in community management. You're an AI developed by Richenel's AI Agency, an AI automation agency.

Purpose: you act as an expert community manager, creating posts describing how AI can help a company manage its social networks.

Characteristic: the posts you write must be written in everyday French, in a friendly, calm and cheerful tone, and addressed to a lambda user to convince them to call on you to manage their social networks.

How it works : Several functions have been designed to help you achieve your goals. First of all, you need to choose a different topic from the one you've already been working on, then save the chosen topic. Finally, you need to generate a publication and an image that perfectly illustrates your post and encourages a user to read the content of your post. The result you need to provide will be a json with the keys "publication" and "image_description".

Reply with "TERMINATE" when you've finished creating the publication.""",

        llm_config=llm_config,
    )

    # create a UserProxyAgent instance named "user_proxy"
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        human_input_mode="NEVER",
        max_consecutive_auto_reply=20,
    )

    # @user_proxy.register_for_execution()
    # @chatbot.register_for_llm(description="generate image an send it to social media")
    # def generate_images_and_post(
    #         post: Annotated[str, "the publication that will be posted on social networks with emojis"],
    #         description: Annotated[str, "hyper detailed description of the image that you want"],
    # )-> str:
    #     client = OpenAI(api_key = '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')

    #     if "\\" in post or "Ã" in post or "©" in post or "\nd" in post or "%C" in post or "�" in post or "&#" in post:
    #         raise Exception("this function requires a publication in the correct format using 'é à è' and emojis")
    #     response = client.images.generate(
    #         model="dall-e-3",
    #         prompt=f'{description}',
    #         size='1024x1024',
    #         n=1
    #     )
    #     # img_data = requests.get(response.data[0].url).content
    #     # if post[0]=='\n':
    #     #     post = post[1:]
    #     # post_linkedin(message=post,image=img_data)
    #     post_facebook(message=post,image_url=response.data[0].url)

    #     return 'Done'


    @user_proxy.register_for_execution()
    @chatbot.register_for_llm(description="save the new topic")
    def save_topic(

            topic: Annotated[str, "the new topic to save"],
    )-> str:
        # topic = bytes(topic, "utf-8").decode("unicode_escape")
        # topic = unquote(topic)
        print(topic)
        with open('subject.json', 'r',encoding='utf-8') as f:
            data = json.load(f)
            data = list(map(lambda a :bytes(a, "utf-8").decode("unicode_escape"),data))
            data.append(topic)
            if len(data)>20:
                data.pop(0)
        with open('subject.json', 'w',encoding='utf-8') as json_file:
            json.dump(data, json_file,ensure_ascii=False, indent=2)
        return "done"

    @user_proxy.register_for_execution()
    @chatbot.register_for_llm(description="get previous topic")
    def previous_topic()-> list:
        with open('subject.json', 'r',encoding='utf-8') as f:
            data = json.load(f)
        return data
    autogen.ConversableAgent._print_received_message = publier

    user_proxy.initiate_chat(
        chatbot,
        message="genere un nouveau post",
        config_list=config_list
    )

def publier(self,message:str,sender):
    print(message)
    isJson = False
    try:
            js = json.loads(message)
            js["publication"]
            isJson=True
    except Exception as e:
        if "json" in message:
            js = "{"+f'{(message.split("{")[-1]).split("}")[0]}'+"}"
            isJson=True
    if isJson:
            js = json.loads(js)
            print(js)
            client = OpenAI(api_key = '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')
            post = js["publication"]
            description = js["image_description"]
            if "\\" in post or "Ã" in post or "©" in post or "\nd" in post or "%C" in post or "�" in post or "&#" in post:
                raise Exception("this function requires a publication in the correct format using 'é à è' and emojis")
            response = client.images.generate(
                model="dall-e-3",
                prompt=f'{description}',
                size='1024x1024',
                n=1
            )
        # img_data = requests.get(response.data[0].url).content
        # if post[0]=='\n':
        #     post = post[1:]
        # post_linkedin(message=post,image=img_data)
            post_facebook(message=post,image_url=response.data[0].url)
if __name__ == '__main__':
    execute()
