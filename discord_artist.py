import discord
import requests
import io
import os
import random

# Nice way to load environment variables for deployments
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
FIREWORKS_API_KEY = os.environ["FIREWORKS_API_KEY"]

# Configure Discord intents for chatting
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

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
        "num_inference_steps": 30,
        "seed": random.randint(0,1000000) 
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
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):    
        prompt = message.clean_content.replace(f'@{client.user.name}', '').strip()

        # Handle cases where the user only mentions the bot with no prompt
        if not prompt:
            await message.channel.send("You mentioned me! What would you like me to draw?")
            return

        # Let the user know you're working on it
        await message.channel.send(f"Drawing `{prompt}`...")
        
        image_data = generate_image(prompt)
        
        if image_data:
            # Send the image back as a file
            await message.channel.send(file=discord.File(fp=io.BytesIO(image_data), filename="output.jpg"))
        else:
            await message.channel.send("Sorry, I failed to generate the image. Please try again.")

# Run the main loop
client.run(DISCORD_TOKEN)