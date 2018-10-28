import requests
import os
from bs4 import BeautifulSoup
from push import pushover, title, user_key

my_username = os.environ.get('IC_USER')
my_password = os.environ.get('IC_PASS')

with requests.Session() as c:
    url = 'https://union.ic.ac.uk/acc/tennis/booking/login'
    c.get(url)
    payload = {'cid_user': my_username, 'cid_pass': my_password}
    c.post(url, data=payload)
    page = c.get('https://union.ic.ac.uk/acc/tennis/booking')
    
#Start scrapping
soup = BeautifulSoup(page.text, 'html.parser')
tables = soup.find_all('table')
for t in tables:
#TODO find the parent tag and display DATE
    for trs in t.find_all('tr'):
        tds = trs.find_all('td')
        a = tds[3].find('a', href=True)
        print (tds[1].text+" level at "+tds[0].text+" is:\t"+tds[3].text.strip())
        if tds[3].text.strip() == 'Full':
            print("\tNot available for booking\n")
        else:
            print ("\turl: "+a['href']+"\n")
            message = "Bookings available at " + tds[0].text
            pushover(title, message, user_key)
