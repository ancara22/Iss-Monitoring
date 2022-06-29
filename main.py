import requests
from datetime import datetime
from smtplib import SMTP
import time

MY_LAT = 51.578136
MY_LNG = 0.100768
MY_EMAIL = "test.acc.python.first@gmail.com"
MY_PASSWORD = "************"


def is_iss_close():
    respons = requests.get(url="http://api.open-notify.org/iss-now.json")
    respons.raise_for_status()
    data = respons.json()

    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LNG-5 <= iss_longitude <= MY_LNG+5:
        return True
    else:
        return False


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }

    date_request = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    date_request.raise_for_status()
    date = date_request.json()

    sunrise = int(date["results"]['sunrise'].split("T")[1].split(":")[0])
    sunset = int(date["results"]['sunset'].split("T")[1].split(":")[0])

    time_now = int(datetime.now().hour)

    if time_now <= sunrise or time_now >= sunset:
        return True
    else:
        return False


def sent_mail():
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="test.acc.python.first@gmail.com",
                            msg="Subject:ISS\n\nIss station is close to you!\n"
                                                                                   "")


while True:
    time.sleep(60)
    if is_dark() and is_iss_close():
        sent_mail()