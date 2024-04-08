import requests
from twilio.rest import Client
import schedule
import time

# OpenWeatherMap API key
api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
city = 'YOUR_CITY'

# Twilio API credentials
account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
twilio_phone_number = 'YOUR_TWILIO_PHONE_NUMBER'
recipient_phone_number = 'YOUR_RECIPIENT_PHONE_NUMBER'

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def send_weather_text():
    weather_data = get_weather()
    weather_description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']

    client = Client(account_sid, auth_token)
    message_body = f"Today's weather in {city}: {weather_description}, Temperature: {temperature}°C, Humidity: {humidity}%"
    
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=recipient_phone_number
    )

    print('Message sent successfully!')

# Schedule daily execution
schedule.every().day.at("08:00").do(send_weather_text)  # Adjust the time as per your preference

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute if it's time to execute the scheduled task
