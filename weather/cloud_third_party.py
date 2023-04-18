import requests, json, sys
from weather.models import DETAILING_TYPES


class WeatherAPI:
    dummy = False
    url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&exclude={exclude}&appid={key}"
    key = "fbb5de0cf2526f0ba2ea28a2f47ef82d"

    def __init__(self, data):
        self.lat = data["lat"]
        self.long = data["long"]
        self.detailing = data["detailing"]

    def openweather(self):
        url = self.url.format(
            lat=self.lat,
            lon=self.long,
            exclude="%s,alerts"
            % ",".join(
                map(
                    lambda y: y[1].lower(),
                    filter(lambda x: x[0] != self.detailing, DETAILING_TYPES),
                )
            ),
            key=self.key,
        )
        print("Fetching URL : ", url)
        data = {}
        try:
            rdata = requests.get(url, headers={"Content-Type": "application/json"})
            rdata.raise_for_status()
            data = rdata.json()
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error : ", errh.args[0])
        except requests.exceptions.ReadTimeout as errrt:
            print("Time out")
        except requests.exceptions.ConnectionError as conerr:
            print("Connection error")
        except requests.exceptions.RequestException as errex:
            print("Exception request")
        # Not passing server side error to client. Data will be empty in case of error.
        return data
