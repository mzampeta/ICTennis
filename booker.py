import requests
import os
from bs4 import BeautifulSoup
from push import pushover, title, user_key
import time

my_username = os.environ.get('IC_USER')
my_password = os.environ.get('IC_PASS')


#return current datetime
def timer():
    t = str(time.strftime("%d/%m/%Y %H:%M:%S %Z"))
    return t

#Start scrapping
def book(tables):
    for t in tables:
        #TODO find the parent tag and display DATES
        for trs in t.find_all('tr'):
            tds = trs.find_all('td')
            #print booking sttus for each category
            #print (tds[1].text+" level at "+tds[0].text.strip()+" is:\t"+tds[3].text.strip())
            if "Advanced" in tds[1].text:
                if "Book" in tds[3].text.strip():
                    a = tds[3].find('a', href=True)
                    #Attempt booking
                    booker = c.get(a['href'])
                    if booker.status_code == 200:
                        message = str(booker.status_code)+":: Booking completed at "+tds[0].text.strip()+" for "+tds[1].text.strip()
                        # print (timer()+": "+message)
                        pushover(title, message, user_key)
                        return 1
                    else:
                        message = str(booker.status_code)+":: Not Booked"
                        pushover(title, message, user_key)
                        return 0
                elif "Cancel" in tds[3].text.strip():
                    message = "Already booked at: " + tds[0].text.strip()+" for "+tds[1].text.strip()
                    # print (timer()+": "+message)
                    # pushover(title, message, user_key)
                    return 0
                elif tds[3].text.strip() == 'Full' or tds[3].text.strip() == "":
                    # message = "Not available for booking at: " + tds[0].text.strip()+" for "+tds[1].text.strip()
                    # print (timer()+": "+message)
                    # pushover(title, message, user_key)
                    return 3
                else:
                    # print ("ERROR check with admin")
                    # message = "ERROR "+tds[1].text.strip()+" at "+tds[0].text.strip()+" is "+tds[3].text.strip()
                    # print (timer()+": "+message)
                    # pushover(title, message, user_key)
                    return 0
            break

#Initiate session
with requests.Session() as c:
    url = 'https://union.ic.ac.uk/acc/tennis/booking/login'
    c.get(url)
    payload = {'cid_user': my_username, 'cid_pass': my_password}
    c.post(url, data=payload)
    for i in range (1,31):
        page = c.get('https://union.ic.ac.uk/acc/tennis/booking')
        soup = BeautifulSoup(page.text, 'html.parser')
        all_tables = soup.find_all('table')
        #Attemp to BOOK
        result = book(all_tables)
        print (result)
        time.sleep(1)







