#Libraries
import httpx
import random
from colorama import Fore
import threading
from msg import randomQuestions
import json
import time

#Headers required to make ngl think that we are a real user and not a bot
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
}

#function to generate random 36 character length device ids 
def deviceid():
    return "".join(
        random.choice("0123456789abcdefghijklmnopqrstuvwxyz-") for i in range(36)
    )

#function for selecting a random proxy every message
def proxy():
    return "http://" + random.choice(list(open("proxies.txt")))

f = []

#main spam function
def spam(target, msg):
    if messagestatus:
        msg = randomQuestions[random.randint(0, len(randomQuestions) - 1)]
    if proxystatus:
        proxy1 = {"http://": proxy().rstrip()}
        client = httpx.Client(headers=headers, proxies=proxy1)
    else:
        client = httpx.Client(headers=headers)
    
    postresp = client.post(
        f"https://ngl.link/api/submit",
        data={
            "username": target,
            "question": msg,
            "deviceId": deviceid,
        } 
    
    )
    f.append(True)
    return postresp.status_code

#main code
threads = []
def handler(totalMsgs, target, message):
    for i in range(totalMsgs):
        t = threading.Thread(target=spam, kwargs={"target": target, "msg": message})
        threads.append(t)
    for i in range(totalMsgs):
        threads[i].start()
    for i in range(totalMsgs):
        threads[i].join()
    start = time.time()
    while len(f) < totalMsgs:
        continue
    print(f"{Fore.RED}Messages got {Fore.WHITE}sent in {(time.time() - start) / 1000} milliseconds!")

with open("config.json") as config:
    data = json.load(config)
    proxystatus = data["proxies"]
    messagestatus = data["randommsgs"]
username = input(f"{Fore.GREEN}Enter full {Fore.BLUE}username(with numbers)\n")
message = "1"
if not messagestatus:
    message = input(f"{Fore.CYAN}Enter the message you want to send\n")

messages = int(input(f"{Fore.RED}Enter the amount of messages you want to be sent to the user\n"))
handler(messages, username, message)

