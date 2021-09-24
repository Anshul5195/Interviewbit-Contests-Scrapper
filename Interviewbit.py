from bs4 import BeautifulSoup
import requests
import threading

page = requests.get('https://www.interviewbit.com/contests/').text
soup = BeautifulSoup(page, 'html.parser')
active_contests = soup.find("div", attrs={"id": "active_contests"}).findAll("a", attrs={"class": ""})
active_contests_end_time = soup.find("div", attrs={"id": "active_contests"}).findAll("div", attrs={
                                                                "class": "info-value"})
upcoming_contests = soup.find("div", attrs={"id": "upcoming_contests"}).findAll("a", attrs={"class": ""})
upcoming_contests_start_time = soup.find("div", attrs={"id": "upcoming_contests"}).findAll("div", attrs={
                                                                "class": "info-value"})
upcoming_contests_end_time_and_duration = []


def fetch_end_time_and_duration_details(a_url):
    web_page = requests.get(a_url).text
    soup_obj = BeautifulSoup(web_page, 'html.parser')
    end_time_and_duration_details = soup_obj.find("div", attrs={"class": "small-screen-detail-box"}).findAll(
                                                                "span", attrs={"class": "info-value"})
    upcoming_contests_end_time_and_duration.append(end_time_and_duration_details)


thread_list = []
for link in upcoming_contests:
    url = "https://www.interviewbit.com" + str(link["href"])
    thread_list.append(threading.Thread(target=fetch_end_time_and_duration_details, args=(url,)))

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()


upcoming_list = []
for link, start_time, end_time in zip(upcoming_contests, upcoming_contests_start_time,
                                      upcoming_contests_end_time_and_duration):
    add_dict = dict()
    add_dict["Name"] = str(link.text)
    add_dict["Platform"] = "Interview Bit"
    add_dict["challenge_type"] = "Contest"
    add_dict["url"] = "https://www.interviewbit.com" + str(link["href"])
    add_dict["start_time"] = str(start_time.text).strip().split('  ')[0]
    add_dict["end_time"] = ' '.join(str(end_time[0].text).strip().split(' ')[:3])
    add_dict["duration"] = str(end_time[1].text).strip()
    upcoming_list.append(add_dict)


active_list = []
for link, end_time in zip(active_contests, active_contests_end_time):
    add_dict = dict()
    add_dict["Name"] = str(link.text)
    add_dict["Platform"] = "Interview Bit"
    add_dict["challenge_type"] = "Contest"
    add_dict["url"] = "https://www.interviewbit.com" + str(link["href"])
    add_dict["end_time"] = str(end_time.text).strip().split('  ')[0]
    active_list.append(add_dict)
    

print(upcoming_list)
print(active_list)

