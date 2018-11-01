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
#TODO find the parent tag and display DATES
    for trs in t.find_all('tr'):
        tds = trs.find_all('td')
        a = tds[3].find('a', href=True)
        print (tds[1].text+" level at "+tds[0].text.strip()+" is:\t"+tds[3].text.strip())
        if tds[3].text.strip() == 'Full' or tds[3].text.strip() == "":
            print("\tNot available for booking\n")
        elif "Cancel" in tds[3].text.strip():
            print ("You have already book a session for "+tds[0].text)
            #TODO push notification with existing booking details
        elif "Advanced" in tds[1].text and "Book" in tds[3].text.strip():
                message = "Bookings available at " + tds[0].text.strip()
                pushover(title, message, user_key)
                #Attempt booking
                book = c.get(a['href'])
                message = str(book.status_code)+" :: Booking completed at "+tds[0].text.strip()
                print (message)
                pushover(title, message, user_key)
                print("\turl: " + a['href'] + "\n")
        else:
            print ("ERROR check with admin")




