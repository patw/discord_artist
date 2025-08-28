import discord
import os
import io
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Nice way to load environment variables for deployments
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

# Initialize Google GenAI client
genai_client = genai.Client(api_key=GOOGLE_API_KEY)

# Configure Discord intents for chatting
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Generate an image using Google Gemini
def generate_image(prompt):
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=[prompt],
        )
        
        # Extract the generated image from the response
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # Convert the image data to PIL Image
                image = Image.open(BytesIO(part.inline_data.data))
                
                # Convert PIL Image back to bytes for Discord
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                return img_byte_arr.getvalue()
        
        return None
        
    except Exception as e:
        print(f"Error generating image: {e}")
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
            await message.channel.send(file=discord.File(fp=io.BytesIO(image_data), filename="generated_image.png"))
        else:
            await message.channel.send("Sorry, I failed to generate the image. Please try again.")

# Run the main loop
client.run(DISCORD_TOKEN)