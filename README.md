# ChatMeteoBot

ChatMeteoBot is a simple chatbot designed to provide real-time weather updates, forecasts, and Air Quality Index (AQI) information for specific locations. The bot is implemented in Python and consists of three main files: `chatbot.py`, `main.py`, and `requirements.txt`.

## Project Files

### 1. `chatbot.py`

This file contains the implementation of the RuleBot class, which handles user interactions and responds to specific commands. Here is a breakdown of the key components:

- **Initialization:**
  - The class has an `__init__` method that sets up the bot's exit commands and defines regex patterns for various user intents, such as starting a discussion, expressing gratitude, asking about the bot's job, checking the weather forecast, checking real-time weather, and querying the Air Quality Index (AQI).

- **Methods:**
  - `chat(user_message)`: Checks if the user's message is an exit command and returns a corresponding exit response. Otherwise, it processes the user's message and returns an appropriate bot response.
  - `match_reply(reply)`: Matches the user's input against predefined patterns and invokes specific methods based on the identified intent.

- **Commands and Responses:**
  - The class includes methods for handling various user intents, such as starting a discussion, expressing gratitude, checking the weather forecast, obtaining real-time weather information, querying the AQI, and describing the bot's job. Additionally, there is a method for handling unmatched queries.

### 2. `main.py`

This file serves as the main application script using Streamlit for the user interface. It initializes an instance of the RuleBot class and handles user input and bot responses. The chat history is maintained in the session state.

## Usage

To run the ChatMeteoBot, ensure you have the required dependencies installed. Run the following command:

```bash
pip install -r requirements.txt
```

Then, execute the `main.py` script:

```bash
streamlit run main.py
```

The application will open in your default web browser, allowing you to interact with ChatMeteoBot.

## Dependencies

The project relies on the following external libraries, specified in `requirements.txt`:

- `streamlit`: Used for creating the web-based user interface.
- `locationtagger`: Provides functionality for extracting location entities from text.
- `requests`: Handles HTTP requests for weather and AQI data.

## Acknowledgments

- The weather and AQI data in the bot's responses is sourced from external APIs, and the bot utilizes the RapidAPI service for weather information.

Feel free to explore, modify, and enhance the code to suit your specific needs or integrate additional features into ChatMeteoBot. If you have any questions or encounter issues, please refer to the documentation of the used libraries or reach out for assistance.
