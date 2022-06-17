""" 
AWS Lambda function that gets data, performs weather checks, and sends emails.
"""

import json
from bs4 import BeautifulSoup as bs
import requests
import os
from dotenv import load_dotenv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3
import csv
import codecs

load_dotenv()
accessKey = os.getenv('AWS_ACCESS_KEY')
accessSecret = os.getenv('AWS_ACCESS_KEY_SECRET')

def sendEmailAWS(weatherCondition, emailRecipient):
    msg = MIMEMultipart()
    msg["Subject"] = "Rain incoming"
    msg["From"] = "samzitestemail@gmail.com"
    msg["To"] = emailRecipient
    
    body = MIMEText(weatherCondition, "plain")
    msg.attach(body)

    ses_client = boto3.client("ses", region_name='us-east-1', aws_access_key_id=accessKey, aws_secret_access_key=accessSecret)
    ses_client.send_raw_email(
        Source="samzitestemail@gmail.com",
        Destinations=[emailRecipient],
        RawMessage={"Data": msg.as_string()}
    )

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
LANGUAGE = "en-US,en;q=0.5"

def get_weather_data(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    
    html = session.get(url)
    soup = bs(html.text, "html.parser")
    
    will_rain = False;
    result = {}
    
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    days = soup.find("div", attrs={"id": "wob_dp"})
    day = days.findAll("div", attrs={"class": "wob_df"})[0]
    temp = day.findAll("span", {"class": "wob_t"})
    precipitation_forecast = soup.findAll("div", {"class": "wob_hw"})
    result['precipitation_hourly'] = []
    
    hours = 0
    
    for div in precipitation_forecast:
        hours += 1
        
        precipitation_hour = div.find("div", {"class": "XwOqJe"})['aria-label']
        result['precipitation_hourly'].append(precipitation_hour)
        
        get_number = div.find("div", {"class": "XwOqJe"}).text
    
        if (get_number != "" and int (get_number[:-1]) > 10):
            will_rain = True
        
        if hours > 24:
            break
    
    result['max-temp'] = temp[0].text
    result['min-temp'] = temp[2].text
    
    return result, will_rain

def lambda_handler(event='', context=''):
    client = boto3.client("s3")
    data = client.get_object(Bucket='ahrain', Key='recipientsInfo.csv')

    for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"])):
        URL = "https://www.google.com/search?q=" + row['city'] + "+weather&oq=" + row['city'] + "+weather&aqs=chrome..69i57.2478j0j4&sourceid=chrome&ie=UTF-8"
        data, rain_check = get_weather_data(URL)
        message = "Here's your forecast for the day:\n"
        
        for i in range(len(data['precipitation_hourly'])):
            message += data['precipitation_hourly'][i] + "\n"
        
        message += "\n\t* Min temp: {0} Fah, {1} Cel\n".format(data['min-temp'], int((int (data['min-temp']) - 32) * 5.0/9.0))
        message += "\t* Max temp: {0} Fah, {1} Cel".format(data['max-temp'], int((int (data['max-temp']) - 32) * 5.0/9.0))
        message += "\nYou can check the weather using the following link: " + URL
        message += "\nHave a nice and dry day!"
        message += "\nAhrain"
        
        if (rain_check):
            print(message)
            sendEmailAWS(message, row['email'])

lambda_handler()

# include google link for viewing
# nice sign-off