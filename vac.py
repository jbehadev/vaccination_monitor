import requests
import time
import schedule 
from html.parser import HTMLParser
import os
from twilio.rest import Client

sites = [
    {'url': 'https://delcocovid.as.me/modernadelco43829', 'type': 21568128, 'calendar': 5081864, 'name': 'Aston'},
    {'url': 'https://delcocovid.as.me/modernadelco43829', 'type': 21568128, 'calendar': 5018248, 'name': 'Delco'},
    {'url': 'https://delcocovid.as.me/pfizerdelco4821', 'type': 21569283, 'calendar': 5246016, 'name': 'Springfield'},
    {'url': 'https://delcocovid.as.me/pfizerdelco4821', 'type': 21569283, 'calendar': 5171032, 'name': 'Radnor'},
]



# Find these values at https://twilio.com/user/account
# To set up environmental variables, see http://twil.io/secure
account_sid = 'X'
auth_token = 'X'
to_phone = '+15558675390'
from_phone = '+15558675309'
to_email = 'test@test.com'
mailgun_api = 'X'
mailgun_url = 'https://api.mailgun.net/v3/sandboxX/messages'
from_email = 'test@mailgun.com'


client = Client(account_sid, auth_token)

# send email
def send_simple_message(name, url):
    client.api.account.messages.create(
        to=to_phone,
        from_=from_phone,
        body="An appt is available at: {}: {}".format(name, url))
    
    return requests.post(
        mailgun_url,
        auth=("api", mailgun_api),
        data={"from": from_email,
            "to": to_email,
            "subject": "Vac Appt Available",
            "text": "An appt is available at: {}: {}".format(name, url)})

# handle http request
def handleRequests(txt, site):
    print(site['name'] + ' Url: ' + site['url'], end="\n")
    parser = MyHTMLParser(site)
    parser.feed(txt)

# handle html parsing
class MyHTMLParser(HTMLParser):
    def __init__(self, site):
        super().__init__()
        self.reset()
        self.site = site

    def handle_data(self, data):
        if data.strip():
            print("Available: ", data)
        if "Earlier Times" in data.strip():
            print('Found')
            send_simple_message(self.site['name'], self.site['url'])


def run_schedule():
    url = 'https://delcocovid.as.me/schedule.php?action=showCalendar&fulldate=1&owner=21717099&template=weekly'

    for site in sites:
        myobj = {
            'type': site['type'],
            'calendar': site['calendar'],
            'skip': True,
            'options[qty]': 1,
            'options[numDays]': 5,
            'ignoreAppointment': '',
            'appointmentType': site['type'],
            'calendarID': ''
        }
        x = requests.post(url, data = myobj)
        handleRequests(x.text, site)

run_schedule()
schedule.every(5).minutes.do(run_schedule)

while True:
    schedule.run_pending()
    time.sleep(1)

