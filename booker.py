import requests
import os
from bs4 import BeautifulSoup
from push import pushover, title, user_key
import time

my_username = os.environ.get('IC_USER')
my_password = os.environ.get('IC_PASS')

def timer():
    t = str(time.strftime("%d/%m/%Y %H:%M:%S %Z"))
    return t

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
#TODO find the parent tag and display DATES
    for trs in t.find_all('tr'):
        tds = trs.find_all('td')
        a = tds[3].find('a', href=True)
        #print booking sttus for each category
        #print (tds[1].text+" level at "+tds[0].text.strip()+" is:\t"+tds[3].text.strip())
        if "Advanced" in tds[1].text:
            if "Cancel" in tds[3].text.strip():
                message = "Already booked at: " + tds[0].text.strip()+" for "+tds[1].text.strip()
                print (timer()+":"+message)
                pushover(title, message, user_key)
            elif tds[3].text.strip() == 'Full' or tds[3].text.strip() == "":
                message = "Not available for booking at: " + tds[0].text.strip()+" for "+tds[1].text.strip()
                print (timer()+":"+message)
                pushover(title, message, user_key)
            elif "Book" in tds[3].text.strip():
                #Attempt booking
                book = c.get(a['href'])
                message = str(book.status_code)+"::Booking completed at :"+tds[0].text.strip()+" for "+tds[1].text.strip()
                print (timer()+":"+message)
                pushover(title, message, user_key)
            else:
                print ("ERROR check with admin")
                message = "ERROR "+tds[1].text.strip()+" at "+tds[0].text.strip()+" is "+tds[3].text.strip()
                print (timer()+":"+message)
                pushover(title, message, user_key)





