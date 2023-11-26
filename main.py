import os

import discord
import json
import dotenv
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# Watson Assistant API credentials
dotenv.load_dotenv()
WATSON_API_KEY = os.environ['WATSON_API_KEY']
WATSON_API_URL = os.environ['WATSON_API_URL']
WATSON_ASSISTANT_ID = os.environ['WATSON_ASSISTANT_ID']

# Discord Bot Token
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

# Discord client
intents = discord.Intents(messages=True, guilds=True, reactions=True, message_content=True)
bot = discord.Client(intents=intents)

# IBM Watson Assistant setup
authenticator = IAMAuthenticator(WATSON_API_KEY)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)

assistant.set_service_url(WATSON_API_URL)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(message.content)

    if message.content.startswith('<@1177864741532741702>'):
        # Extract the user's input from the message
        user_input = message.content[23:]

        # Call Watson Assistant API
        response = watson_assistant(user_input)

        # Send Watson's response to the Discord channel
        await message.channel.send(response)


# Function to make a request to Watson Assistant API
def watson_assistant(user_input):
    # Create a session
    session_response = assistant.create_session(assistant_id=WATSON_ASSISTANT_ID).get_result()
    session_id = session_response["session_id"]

    # Interact with the assistant using the session
    response = assistant.message(
        assistant_id=WATSON_ASSISTANT_ID,
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': user_input
        }
    ).get_result()

    print(json.dumps(response, indent=2))

    # Close the session
    assistant.delete_session(assistant_id=WATSON_ASSISTANT_ID, session_id=session_id)

    return response['output']['generic'][0]['text']

# Run the bot
bot.run(DISCORD_TOKEN)
