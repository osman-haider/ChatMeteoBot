import random
import re
import requests
import locationtagger
from datetime import date, timedelta, datetime


class RuleBot:
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later", "by")

    def __init__(self):
        self.matches = {'start_discussion': r'.*\s*(hi|hello|helo|how are you|hey|hi there|hye),*',
                        'thanks': r'.*\s*(good|well done|nice|nice work|grate job|thanks|thank you so much|thanks dear|love you|thank you),*',
                        'describe_your_job': r'.*\s*(your job|your role|your work|your self|tell me about your),*',
                        'forcast_weather': r'.*\s*(forecast weatherr|weather forecast),*',
                        'real_time_weather': r'.*\s*(temperature in|temperature|the temperature|wind|clouds|cloud|winds|weather|complete weather|weather report|current weather report|current weather),*',
                        'aqi': r'.*\s*(aqi|AQI|Air quality index|air quality index|air quality|Air quality),*'
                        }

    def chat(self, user_message):
        for command in self.exit_commands:
            if user_message == command:
                exit_responses = (
                    "Thank you for using the weather and AQI chatbot! If you have more questions in the future, feel free to return. Goodbye!",
                    "It was a pleasure assisting you! If you ever need weather or air quality information again, don't hesitate to reach out. Goodbye!",
                    "Goodbye! If you require further assistance or have more inquiries, feel free to come back anytime.",
                    "Thank you for chatting! If there's anything else you'd like to know in the future, feel free to ask. Goodbye!",
                    "It's been a pleasure helping you with weather and air quality information. If you have more questions later on, feel free to return. Goodbye!"
                )
                return random.choice(exit_responses)
        # Process user's message
        bot_response = self.match_reply(user_message)
        return bot_response

    def match_reply(self, reply):
        for key, value in self.matches.items():
            intent = key
            regex_pattern = value
            found_match = re.match(regex_pattern, reply)
            if found_match and intent == 'start_discussion':
                return self.start_discussion()
            elif found_match and intent == 'thanks':
                return self.thanks()
            elif found_match and intent == 'real_time_weather':
                return self.real_time_weather(reply)
            elif found_match and intent == 'forcast_weather':
                return self.forcast_weather(reply)
            elif found_match and intent == 'aqi':
                return self.aqi(reply)
            elif found_match and intent == 'describe_your_job':
                return self.describe_your_job()
        if not found_match:
            return self.no_match()

    def start_discussion(self):
        greeting_responses = (
            "Hello! Welcome to WeatherAQI-Bot. How can I assist you today?",
            "Hi there! I'm here to provide you with weather and air quality information. What can I help you with?",
            "Greetings! Feel free to ask me about the weather, air quality, or anything related. I'm here to assist you.",
            "Hello! It's great to have you here. If you have any questions about the weather or air quality, just let me know.",
            "Hi! I'm your weather and air quality assistant. What information are you looking for today?",
            "Hello and welcome! I'm here to provide you with real-time weather updates and air quality information. How can I assist you?",
            "Hi, how can I help you today? Feel free to ask about the weather, air quality, or anything else you're curious about.",
            "Greetings! I'm here to keep you informed about the latest weather conditions and air quality. What can I do for you?",
            "Hello! If you're curious about the weather or air quality in a specific location, just let me know, and I'll provide the details.",
            "Hi there! I'm your virtual weather assistant. Ask me anything about the weather or air quality, and I'll do my best to help."
        )
        return random.choice(greeting_responses)

    def aqi(self,value):
        place_entity = locationtagger.find_locations(text=value)
        if place_entity.cities:
            city = place_entity.cities[0]
            url = "https://api.waqi.info/feed/{}/?token=17d10ac786fa7ba766e84aeda4d949cdd4d28fd4".format(city)
            response = requests.get(url)
            data = response.json()
            aqi_value = data['data']['aqi']

            def interpret_aqi(aqi_value):
                if 0 <= aqi_value <= 50:
                    return "Good"
                elif 51 <= aqi_value <= 100:
                    return "Moderate"
                elif 101 <= aqi_value <= 150:
                    return "Unhealthy for Sensitive Groups"
                elif 151 <= aqi_value <= 200:
                    return "Unhealthy"
                elif 201 <= aqi_value <= 300:
                    return "Very Unhealthy"
                else:
                    return "Hazardous"
            responses = (f'Great! The current Air Quality Index (AQI) for {city} is {aqi_value}. The air quality is considered to be {interpret_aqi(aqi_value)}.\n',
                         f'Sure thing! In {city}, the current AQI is {aqi_value}. This corresponds to {interpret_aqi(aqi_value)} air quality.\n',
                         f'Thanks for providing the city. As of now, the AQI in {city} is {aqi_value}. It indicates {interpret_aqi(aqi_value)} air quality.\n',
                         f'Got it! The current Air Quality Index (AQI) in {city} is {aqi_value}. This suggests {interpret_aqi(aqi_value)} air quality.\n',
                         f"Excellent! I've checked the AQI for {city}, and it's currently {aqi_value}. The air quality level is {interpret_aqi(aqi_value)}.\n")
            return random.choice(responses)

        else:
            responses = ("Sure, I can help you check the AQI. To provide accurate information, could you please enter the name of the city you'd like to check?\n",
                         "Great! I'd be happy to check the AQI for you. To proceed, could you kindly specify the city for which you want to know the Air Quality Index?\n",
                         "Certainly! To check the AQI, I just need to know the city you're interested in. Could you please enter the name of the city?\n",
                         "No problem! I can help you with that. Before we proceed, could you tell me the name of the city for which you'd like to check the Air Quality Index?\n",
                         "Certainly, I can assist with that. To get accurate AQI information, could you please provide the name of the city you want to check?\n")
            return random.choice(responses)

    def forcast_weather(self,value):
        place_entity = locationtagger.find_locations(text=value)
        if place_entity.cities:
            city = place_entity.cities[0]
            udate = re.findall('\d{4}-\d{2}-\d{2}', value)
            if udate:
                udate = udate[0]
                user_date = datetime.strptime(udate, '%Y-%m-%d').date()
                today_date = date.today()
                treshold = 10
                delta = timedelta(days=treshold)
                ending_date = today_date + delta
                if ending_date > user_date and user_date >today_date:
                    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
                    headers = {
                        "X-RapidAPI-Key": "d29f4e2eb5mshc2e8f0289f74ce9p13a165jsnbc36640cc6b5",
                        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
                    }

                    params = {
                        "q": city,
                        "dt": user_date,
                    }

                    try:
                        response = requests.get(url, headers=headers, params=params)
                        response.raise_for_status()  # Raise an HTTPError for bad responses
                        data = response.json()
                        dowling = ""

                        time_pattern = r'\b\d{1,2}(?:AM|PM)\b'
                        hour = re.findall(time_pattern, value)
                        if hour:

                            # Initialize the 'dowling' variable as a list to store the data
                            dowling = []

                            # Extracting current time data
                            current_time_data = next(
                                (hour for hour in data['forecast']['forecastday'][0]['hour'] if
                                 hour['time'] == '2023-12-10 00:00'),
                                None
                            )

                            if current_time_data:
                                current_time_info = {
                                    "Time": current_time_data['time'],
                                    "Temperature": f"{current_time_data['temp_c']}°C",
                                    "Cloud": f"{current_time_data['cloud']}%",
                                    "Wind": f"{current_time_data['wind_kph']} kph",
                                    "Humidity": f"{current_time_data['humidity']}%"
                                }
                                dowling.append(current_time_info)

                            # Extracting and storing data for the next 24 hours
                            for hour_data in data['forecast']['forecastday'][0]['hour']:
                                hour_info = {
                                    "Time": hour_data['time'],
                                    "Temperature": f"{hour_data['temp_c']}°C",
                                    "Cloud": f"{hour_data['cloud']}%",
                                    "Wind": f"{hour_data['wind_kph']} kph",
                                    "Humidity": f"{hour_data['humidity']}%"
                                }
                                dowling.append(hour_info)

                            hour = hour[0]
                            h = hour
                            if hour == '12AM':
                                hour = '00:00'
                            elif hour == '1AM' or hour == '01AM':
                                hour = '01:00'
                            elif hour == '2AM' or hour == '02AM':
                                hour = '02:00'
                            elif hour == '3AM' or hour == '03AM':
                                hour = '03:00'
                            elif hour == '4AM' or hour == '04AM':
                                hour = '04:00'
                            elif hour == '5AM' or hour == '05AM':
                                hour = '05:00'
                            elif hour == '6AM' or hour == '06AM':
                                hour = '06:00'
                            elif hour == '7AM' or hour == '07AM':
                                hour = '07:00'
                            elif hour == '8AM' or hour == '08AM':
                                hour = '08:00'
                            elif hour == '9AM' or hour == '09AM':
                                hour = '09:00'
                            elif hour == '10AM':
                                hour = '10:00'
                            elif hour == '11AM':
                                hour = '11:00'
                            elif hour == '12PM':
                                hour = '12:00'
                            elif hour == '1PM' or hour == '01PM':
                                hour = '13:00'
                            elif hour == '2PM' or hour == '02PM':
                                hour = '14:00'
                            elif hour == '3PM' or hour == '03PM':
                                hour = '15:00'
                            elif hour == '4PM' or hour == '04PM':
                                hour = '16:00'
                            elif hour == '5PM' or hour == '05PM':
                                hour = '17:00'
                            elif hour == '6PM' or hour == '06PM':
                                hour = '18:00'
                            elif hour == '7PM' or hour == '07PM':
                                hour = '19:00'
                            elif hour == '8PM' or hour == '08PM':
                                hour = '20:00'
                            elif hour == '9PM' or hour == '09PM':
                                hour = '21:00'
                            elif hour == '10PM' or hour == '10PM':
                                hour = '22:00'
                            elif hour == '11PM' or hour == '11PM':
                                hour = '23:00'
                            
                            target_hour = f'{udate} {hour}'
                            filtered_data = [info for info in dowling if info['Time'] == target_hour]
                            show = ""
                            for s in filtered_data:
                                for key, value in s.items():
                                    show += f"{key}: {value}\n\n "
                            #return f'On {udate} at {h}, here is the weather forecast for {city}. \n\n {show}'
                            response = (
                                f"On {udate} at {h}, here is the detailed weather forecast for {city}:\n\n"
                                f"{show}\n"
                                f"Please note that weather conditions may change, and it's always a good idea to check for updates closer to the specified time."
                            )
                            return response

                        else:
                            # Extracting and storing data for the next 24 hours
                            for hour_data in data['forecast']['forecastday'][0]['hour']:
                                hour_info = (
                                    f"Time ({hour_data['time']}):\n"
                                    f"Temperature: {hour_data['temp_c']}°C, "
                                    f"Cloud: {hour_data['cloud']}%, "
                                    f"Wind: {hour_data['wind_kph']} kph, "
                                    f"Humidity: {hour_data['humidity']}%\n\n"
                                )
                                dowling += hour_info
                            return  dowling

                    except requests.exceptions.RequestException as err:
                        return f"Error: {err}"

                else:
                    return "Please ensure that your specify date is grater then today date for the weather forecast, ensuring that your new date must be within 10 days."
            else:
                return "Please ensure you specify the correct date for the weather forecast, ensuring that the provided date is like YYYY-MM-DD."
        else:
            return "Please ensure that you provide the name of the city for Weather Forecast information, and make sure the first letter of the city name is capitalized."


    def real_time_weather(self,value):
        place_entity = locationtagger.find_locations(text=value)
        if place_entity.cities:
            city = place_entity.cities[0]
            url = "https://weatherapi-com.p.rapidapi.com/current.json"
            headers = {
                'X-RapidAPI-Key': 'd29f4e2eb5mshc2e8f0289f74ce9p13a165jsnbc36640cc6b5',
                'X-RapidAPI-Host': 'weatherapi-com.p.rapidapi.com'
            }
            params = {
                'q': city
            }
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()  # Check if the request was successful
                data = response.json()

                temp = "temperature"
                cloud = "cloud"
                wind = "wind"
                complete = "complete"
                val = None
                if temp in value:
                    for key, value in data.items():
                        if key and 'temp_c' in value:
                            val = data.get(key, {}).get('temp_c', 0)
                    return f'Temperature in {city} is {val}'
                elif cloud in value:
                    for key, value in data.items():
                        if key and 'cloud' in value:
                            val = data.get(key, {}).get('cloud', 0)
                    if val == 0:
                        return f'No cloud in city {city}'
                    else:
                        return f'Clouds are is city {city} are {val}%'
                elif wind in value:
                    for key, value in data.items():
                        if key and 'wind_kph' in value:
                            val = data.get(key, {}).get('wind_kph', 0)
                        return f'Wind in your city {city} is {val}'
                elif complete in value:
                    def flatten_dict(d, parent_key='', sep='_'):
                        items = []
                        for k, v in d.items():
                            new_key = f'{parent_key}{sep}{k}' if parent_key else k
                            if isinstance(v, dict):
                                items.extend(flatten_dict(v, new_key, sep=sep).items())
                            else:
                                items.append((new_key, v))
                        return dict(items)

                    flat_data = flatten_dict(data)
                    output_string = ', \n\n'.join([f'{key}: {value}' for key, value in flat_data.items()])
                    return output_string
                else:
                    w=None
                    c=None
                    t=None
                    for key, value in data.items():
                        if key and 'wind_kph' in value:
                            w = data.get(key, {}).get('wind_kph', 0)
                            c = data.get(key, {}).get('cloud', 0)
                            t = data.get(key, {}).get('temp_c', 0)
                    return f'The temperature in {city} is currently at {t} degrees Celsius, with {c}% clouds in the sky, and a gentle breeze blowing at {w} kilometers per hour'

            except requests.exceptions.RequestException as e:
                return e
        else:
            return "Please ensure that you provide the name of the city for real-time weather information, and make sure the first letter of the city name is capitalized."

    def describe_your_job(self):
        responses = (
            "I'm a weather and air quality chatbot. My main job is to provide you with real-time weather updates, forecasts, and Air Quality Index (AQI) information for any location you're interested in. How can I assist you today?\n",
            "I'm your go-to source for weather and air quality information! Whether you need to know the current conditions, forecast, or AQI for a specific location, just ask, and I'll provide you with the latest updates.\n",
            "Nice to meet you! I'm a weather and AQI chatbot designed to keep you informed about the atmospheric conditions. Feel free to ask me about the weather, forecasts, or air quality in any city around the world.\n",
            "I'm here to keep you informed about the weather and air quality. You can ask me about the current conditions, forecasts, or AQI for any city, and I'll provide you with the most up-to-date information available.\n",
            "I'm your virtual weather assistant! I specialize in providing real-time weather updates and forecasts, along with Air Quality Index (AQI) information. Just let me know what city you're interested in, and I'll do the rest\n",
            "I'm a weather and AQI chatbot. My primary function is to help you stay updated on weather conditions and air quality levels. Ask me anything related to the weather or AQI, and I'll do my best to provide you with accurate information.\n",
            "I'm all about weather and air quality! Whether you want to know if you need an umbrella today or check the air quality in your city, I've got you covered. What can I help you with?\n",
            "Greetings! I'm a specialized chatbot designed to deliver real-time weather updates and forecasts, including information on the Air Quality Index. Feel free to ask me about the weather or air quality for any location you have in mind.\n",
            "I'm your personal weather and air quality companion! If you're curious about the current weather, upcoming forecast, or want to know about the Air Quality Index in a specific location, just ask, and I'll share the details with you.\n")
        return random.choice(responses)


    def no_match(self):
        responses = (
            "I'm sorry, I'm designed to provide information about weather and air quality. If you have any questions related to that, feel free to ask!",
            "That's an interesting question, but my expertise lies in weather and air quality. If you have queries in that domain, I'm here to help!",
            "It seems like you've asked something outside my current capabilities. I'm here to assist with weather and air quality information. Let me know if you have any related questions!",
            "I appreciate your curiosity! However, my focus is on delivering weather and air quality updates. If you have any questions in those areas, feel free to ask away!",
            "While I can't answer that specific question, I'm here to provide you with the latest weather and air quality information. What location are you interested in?",
            "Your question is intriguing, but unfortunately, it's beyond the scope of my current capabilities. I'm best at answering queries about weather and air quality. How can I assist you in those areas?",
            "I'm afraid I don't have the information you're looking for. My expertise is in weather and air quality. If you have questions related to that, I'm at your service!",
            "It seems like your question is outside the scope of my current abilities. I'm here to help with weather and air quality information. What city or region are you interested in?",
            "I'm here specifically for weather and air quality-related queries. If you have a question in those domains, feel free to ask, and I'll do my best to assist you!",
            "While I can't address that particular question, I'm here to provide you with real-time weather updates and air quality information. What city or location would you like details about?"
            )
        return random.choice(responses)

    def thanks(self):
        responses = (
            "No problem at all! If there's anything else you'd like to know, just let me know.",
            "I'm glad I could help! If you ever need weather or air quality updates again, don't hesitate to reach out.",
            "You're very welcome! Should you have any more inquiries or require assistance, I'm here for you.",
            "It was my pleasure! If there's anything else on your mind, feel free to ask anytime.",
            "Anytime! If you have more questions in the future or need information, feel free to drop by.",
            "I'm here to assist! If there's anything else you'd like to know, feel free to ask for more information.",
            "You're welcome! Stay informed, and if there's anything else you need, I'm here to help.",
            "The pleasure is mine! If there's anything specific you're curious about, feel free to ask for more details.",
            "Not a problem! If you have additional questions or need updates in the future, don't hesitate to reach out."
        )
        return random.choice(responses)