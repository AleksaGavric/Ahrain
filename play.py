from bs4 import BeautifulSoup as bs
import requests

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
        get_number = div.find("div", {"class": "XwOqJe"}).text
        
        if (get_number[:-1] != "" and int (get_number[:-1]) > 10):
            info = precipitation_hour.split(" ")
            result['precipitation_hourly'].append("Drizzle at {time}{am}: {chance} chance".format(time = info[2], am = info[3], chance = info[0]))    
            will_rain = True
            continue
           
        if (get_number[:-1] != "" and int (get_number[:-1]) > 12):
            result['precipitation_hourly'].append(precipitation_hour)    
            will_rain = True
            continue
        
        if (get_number[:-1] != "" and int (get_number[:-1]) > 15):
            result['precipitation_hourly'].append("precipitation_hour")    
            will_rain = True 
            continue
         
        if hours > 24:
            break
    
    result['max-temp'] = temp[0].text
    result['min-temp'] = temp[2].text
    
    return result, will_rain

URL = "https://www.google.com/search?q=rochester+weather&client=safari&rls=en&ei=kkqxYqPqOvLQkPIP3OSokAk&ved=0ahUKEwij-6OB3L34AhVyKEQIHVwyCpIQ4dUDCA4&oq=rochester+weather&gs_lcp=Cgdnd3Mtd2l6EAwyBwgAEEcQsAMyCggAEEcQsAMQyQMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAELADEEMyBwgAELADEEMyBwgAELADEEMyBwgAELADEEMyCggAEOQCELADGAEyCggAEOQCELADGAEyCggAEOQCELADGAEyCggAEOQCELADGAEyCggAEOQCELADGAFKBAhBGABKBAhGGAFQAFgAYOw7aAJwAXgAgAEAiAEAkgEAmAEAyAERwAEB2gEGCAEQARgJ&sclient=gws-wiz"
data, rain_check = get_weather_data(URL)

message = "\n"

for i in range(len(data['precipitation_hourly'])):
    message += data['precipitation_hourly'][i] + "\n"

message += "\n* Min temp: {0} Fah, {1} Cel\n".format(data['min-temp'], int((int (data['min-temp']) - 32) * 5.0/9.0))
message += "* Max temp: {0} Fah, {1} Cel \n\n".format(data['max-temp'], int((int (data['max-temp']) - 32) * 5.0/9.0))

if (rain_check):
    print(message)
            


