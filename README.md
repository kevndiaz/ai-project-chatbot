# AI Project Chatbot

## Description

This project includes three chatbots implemented for Discord, Slack, and Telegram, as well as a cloud function for performing Google Custom Search. Each bot leverages IBM Watson Assistant for natural language processing, and the cloud function uses Google Custom Search API to find relevant links.

## Bots

### Discord Bot

File: `bots/discord-bot.py`

#### Requirements

- `discord`
- `ibm-watson`
- `python-dotenv`

#### Usage

1. Install the required dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with the following variables:
    - `WATSON_API_KEY`: Your Watson Assistant API key
    - `WATSON_API_URL`: Your Watson Assistant API URL
    - `WATSON_ASSISTANT_ID`: Your Watson Assistant ID
    - `DISCORD_TOKEN`: Your Discord bot token
3. Run the Discord bot: `python discord-bot.py`

### Slack Bot

File: `bots/slack-bot.py`

#### Requirements

- `slack`
- `flask`
- `slackclient`
- `slackeventsapi`
- `ibm-watson`
- `python-dotenv`

#### Usage

1. Install the required dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with the following variables:
    - `WATSON_API_KEY`: Your Watson Assistant API key
    - `WATSON_API_URL`: Your Watson Assistant API URL
    - `WATSON_ASSISTANT_ID`: Your Watson Assistant ID
    - `SLACK_TOKEN`: Your Slack bot token
    - `SLACK_SIGNING_SECRET`: Your Slack signing secret
3. Run the Slack bot: `python slack-bot.py`

### Telegram Bot

File: `bots/telegram-bot.py`

#### Requirements

- `pyTelegramBotAPI`
- `ibm-watson`
- `python-dotenv`

#### Usage

1. Install the required dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with the following variables:
    - `WATSON_API_KEY`: Your Watson Assistant API key
    - `WATSON_API_URL`: Your Watson Assistant API URL
    - `WATSON_ASSISTANT_ID`: Your Watson Assistant ID
    - `TELEGRAM_API_TOKEN`: Your Telegram bot token
3. Run the Telegram bot: `python telegram-bot.py`

## Cloud Function

File: `cloud-functions/cloud-function.py`

#### Requirements

- `requests`

#### Usage

1. Create a `.env` file with the following variables:
    - `GOOGLE_API_KEY`: Your Google API key
    - `SEARCH_ENGINE_ID`: Your Google Custom Search Engine ID
2. Deploy the cloud function to your preferred serverless platform.

## Dependencies

File: `requirements.txt`

Install all dependencies at once using: `pip install -r requirements.txt`
