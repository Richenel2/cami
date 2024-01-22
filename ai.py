
from openai import OpenAI
import autogen
from linkedIn import post_linkedin
from typing_extensions import Annotated
import json
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
    }
    chatbot = autogen.AssistantAgent(
        name="chatbot",
        system_message="You are an expert in managing the linkedin page of Richenel's AI Agency, a company that automates processes via AI for its clients. In order to get more customers and attract subscribers, you need to write a linkendin post that is interesting to read for an average user and that will encourage them to contact us for our services. You will choose a new random topic that is different to the topics that have already been used but it must be interesting and easy to read for the user with very few complex terms. then you will save the newly chosen topic using the given function. you will also have to generate an image via the given function describing in detail the image that will be the most captivating for the chosen topic and also sending the whole post that has been generated without any modification to the function. reply with TERMINATE when you have finished.",
        llm_config=llm_config,
    )

    # create a UserProxyAgent instance named "user_proxy"
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
    )

    @user_proxy.register_for_execution()
    @chatbot.register_for_llm(description="generate image an post the massa")
    def generate_images_and_post(
            linkindIn_post: Annotated[str, "the complete linkedin post"],
            description: Annotated[str, "hyper detailed description of the image that you want"],
    )-> str:
        client = OpenAI(api_key = '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')

        response = client.images.generate(
            model="dall-e-3",
            prompt=f'{description}',
            size='1024x1024',
            n=1
        )
        img_data = requests.get(response.data[0].url).content
        if linkindIn_post[0]=='\n':
            linkindIn_post = linkindIn_post[1:]
        post_linkedin(message=linkindIn_post,image=img_data)

        return 'Done'


    @user_proxy.register_for_execution()
    @chatbot.register_for_llm(description="save the new topic")
    def save_topic(

            topic: Annotated[str, "the new topic to save"],
    )-> str:
        with open('subject.json', 'r') as f:
            data = json.load(f)
            data.append(topic)
            if len(data)>20:
                data.pop(0)
        with open('subject.json', 'w') as json_file:
            json.dump(data, json_file)
        return "done"

    @user_proxy.register_for_execution()
    @chatbot.register_for_llm(description="get previous topic")
    def previous_topic(
    )-> list:
        with open('subject.json', 'r') as f:
            data = json.load(f)
        return data


    user_proxy.initiate_chat(
        chatbot,
        message="genere un nouveau post ",
        config_list=config_list
    )

if __name__ == '__main__':
    execute()
