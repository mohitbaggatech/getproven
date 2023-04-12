import requests, json
from weather.models import DETAILING_TYPES

class WeatherAPI:
    test = True

    def __init__(self, data):
        self.lat = data['lat']
        self.long = data['long']
        self.detailing = data['detailing']


    def openweather(self):
        url = 'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={key}'\
          .format(
            lat=self.lat, lon=self.long,
            exclude="%s,alerts"%\
            ",".join(map(lambda y: y[1].lower(), filter(lambda x: x[0] != self.detailing, DETAILING_TYPES))),
            key="fbb5de0cf2526f0ba2ea28a2f47ef82d"
          )
        print(url)
        rdata = requests.get(url)
        if self.test:
            data = json.load(open('weather/dummy_openweather_response.json')) if self.test else rdata
        elif rdata.status_code != requests.codes.ok:
            data = {'error': "Error Fetching OPEN WEATHER API DATA.  Status Code : %s"%rdata.status_code}
        else:
            data = rdata.json()
            try:
                data = data[list(filter(lambda x: x[0] == self.detailing, DETAILING_TYPES))[0][1].lower()]
            except:
                data = {'error': "Raise relevant error"}
        return data

    def fetch_data(self):
        return self.openweather()


