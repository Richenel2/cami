
from openai import AzureOpenAI

client = AzureOpenAI(
azure_endpoint= "https://kayra.openai.azure.com/",
api_version = "2023-06-01-preview",
api_key = '4535137c97f24af9b7044efe51b598b6')

response = client.images.generate(
    prompt='Create an image with black background, a happy robot is showing a sign with "I Love AutoGen"',
    size='1024x1024',
    n=1
)

image_url = response["data"][0]["url"]
