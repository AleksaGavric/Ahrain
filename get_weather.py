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
    
    result = {}
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    
    return result

if __name__ == "__main__":
    URL = "https://www.google.com/search?q=charlotte+weather&oq=charlotte+weather&aqs=chrome..69i57.2478j0j4&sourceid=chrome&ie=UTF-8"
    data = get_weather_data(URL)
    
    print("\nNow:", data["dayhour"])
    print("Description:", data['weather_now'])
