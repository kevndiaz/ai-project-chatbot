import os
import slack
import json
import dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load environment variables from .env file
dotenv.load_dotenv()

# Watson Assistant API credentials
WATSON_API_KEY = os.environ['WATSON_API_KEY']
WATSON_API_URL = os.environ['WATSON_API_URL']
WATSON_ASSISTANT_ID = os.environ['WATSON_ASSISTANT_ID']

# Slack Bot Token
SLACK_TOKEN = os.environ['SLACK_TOKEN']

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=SLACK_TOKEN)
BOT_ID = client.api_call('auth.test')['user_id']

# IBM Watson Assistant setup
authenticator = IAMAuthenticator(WATSON_API_KEY)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url(WATSON_API_URL)


@slack_event_adapter.on('message')
def message(payload):
    """
    Event handler for Slack messages.

    Args:
        payload (dict): The payload received from the Slack API.
    """
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if user_id == BOT_ID:
        # Ignore messages sent by the bot itself
        return

    if text.startswith(f'<@{BOT_ID}>'):
        # Extract the user's input from the message
        user_input = text[15:]

        # Call Watson Assistant API
        response = watson_assistant(user_input)

        # Send Watson's response to the Slack channel
        client.chat_postMessage(channel=channel_id, text=response)
        print("BOT_ID: " + BOT_ID)


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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
