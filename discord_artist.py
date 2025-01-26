import discord
import requests
import re
import os

# Nice way to load environment variables for deployments
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
FIREWORKS_API_KEY = os.environ["FIREWORKS_API_KEY"]

# Configure Discord intents for chatting
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Removes discord IDs from strings
def remove_id(text):
    return re.sub(r'<@\d+>', '', text)

# Generate an image using the Flux Dev model
def generate_image(prompt):
    url = "https://api.fireworks.ai/inference/v1/workflows/accounts/fireworks/models/flux-1-dev-fp8/text_to_image"
    headers = {
        "Content-Type": "application/json",
        "Accept": "image/jpeg",
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
    }
    data = {
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "guidance_scale": 3.5,
        "num_inference_steps": 30
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.content
    else:
        print("Error:", response.status_code, response.text)
        return None

@client.event
async def on_ready():
    print(f'Bot logged in as {client.user}')

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        prompt = remove_id(message.content)
        await message.channel.send(F"Drawing {prompt}...")
        image_data = generate_image(prompt)
        if image_data:
            with open("output.jpg", "wb") as f:
                f.write(image_data)
            await message.channel.send(file=discord.File("output.jpg"))
        else:
            await message.channel.send("Failed to generate the image. Please try again.")

# Run the main loop
client.run(DISCORD_TOKEN)