import json
# import requests
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
accessSecret = os.getenv('AWS_SECRET_ACCESS_KEY')

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



def lambda_handler(event, context):
    URL = "https://www.google.com/search?q=charlotte+weather&oq=charlotte+weather&aqs=chrome..69i57.2478j0j4&sourceid=chrome&ie=UTF-8"
    data = get_weather_data(URL)
    
    print("\nNow:", data["dayhour"])
    print("Description:", data['weather_now'])

    #sendEmailAWS(data['weather_now'])
    sendEmailAWS(data['weather_now'])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello from Ahrain!",
            # "location": ip.text.replace("\n", "")
        }),
    }

def get_weather_data(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    
    html = session.get(url)
    soup = bs(html.text, "html.parser")
    
    result = {}
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    
    return result
