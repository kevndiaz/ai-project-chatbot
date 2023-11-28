import os
import discord
import json
import dotenv
import telebot
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load environment variables from .env file
dotenv.load_dotenv()

# Watson Assistant API credentials
WATSON_API_KEY = os.environ['WATSON_API_KEY']
WATSON_API_URL = os.environ['WATSON_API_URL']
WATSON_ASSISTANT_ID = os.environ['WATSON_ASSISTANT_ID']

# Telegram Bot Token
TELEGRAM_API_TOKEN = os.environ['TELEGRAM_API_TOKEN']

# Initialize the Telegram bot
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# IBM Watson Assistant setup
authenticator = IAMAuthenticator(WATSON_API_KEY)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url(WATSON_API_URL)

@bot.message_handler()
def on_message(message):
    """
    Event handler for Telegram messages.

    Args:
        message (telebot.types.Message): The Telegram message object.
    """
    response = watson_assistant(message.text)

    # Send Watson's response to the Telegram chat
    bot.send_message(message.chat.id, response)

# Function to make a request to Watson Assistant API
def watson_assistant(user_input):
    """
    Call Watson Assistant API with user input and return the response.

    Args:
        user_input (str): User's input.

    Returns:
        str: Watson Assistant's response text.
    """
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

# Start polling for new messages
bot.polling()
