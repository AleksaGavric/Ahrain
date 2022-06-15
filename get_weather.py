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
load_dotenv()

accessKey = os.getenv('AWS_ACCESS_KEY')
accessSecret = os.getenv('AWS_ACCESS_KEY_SECRET')

#sends email using SES Amazon email service
def sendEmailAWS(weatherCondition):
    msg = MIMEMultipart()
    msg["Subject"] = "Weather today"
    msg["From"] = "samzitestemail@gmail.com"
    msg["To"] = "samzitestemail@gmail.com"
    
    # Set message body
    body = MIMEText(weatherCondition, "plain")
    msg.attach(body)
 
    # Convert message to string and send
    ses_client = boto3.client("ses", region_name='us-east-1', aws_access_key_id=accessKey, aws_secret_access_key=accessSecret)
    response = ses_client.send_raw_email(
        Source="samzitestemail@gmail.com",
        Destinations=["samzitestemail@gmail.com"],
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
    
    result = {}
    will_rain = True;
    
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    
    days = soup.find("div", attrs={"id": "wob_dp"})
    day = days.findAll("div", attrs={"class": "wob_df"})[0]
    temp = day.findAll("span", {"class": "wob_t"})
    
    result['max-temp'] = temp[0].text
    result['min-temp'] = temp[2].text
    
    return result, will_rain

if __name__ == "__main__":
    URL = "https://www.google.com/search?q=charlotte+weather&oq=charlotte+weather&aqs=chrome..69i57.2478j0j4&sourceid=chrome&ie=UTF-8"
    data, rain_check = get_weather_data(URL)
    
    message = ""
    message += "Min temp: {0} Fah, {1} Cel".format(data['min-temp'], int((int (data['min-temp']) - 32) * 5.0/9.0))
    message += "\nMax temp: {0} Fah, {1} Cel".format(data['max-temp'], int((int (data['max-temp']) - 32) * 5.0/9.0))
    
    if (rain_check):
        print(message)
        sendEmailAWS(message)

