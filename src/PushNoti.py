import requests
import os

"""
Class to send notifications 
"""
class PushNoti:
    def __init__(self, url, deviceName, door):
        self.PUSHOVER_API_URL = url
        self.TOKEN = os.getenv("PUSHOVER_TOKEN")
        #print(os.getenv("PUSHOVER_TOKEN"))
        self.USER = os.getenv("PUSHOVER_USER")
        #print(os.getenv("PUSHOVER_USER"))
        self.DEVICE_NAME = deviceName
        self.MESSAGE = "Your next door is door number " + str(door)

        self.data = {
            "token": self.TOKEN,
            "user": self.USER,
            "message": self.MESSAGE,
            "title": "T.R.U.C.K. Notification",
            "device": self.DEVICE_NAME, 
        }

    def send_message(self):
        response = requests.post(self.PUSHOVER_API_URL, data=self.data)
        print(response.json())

# if __name__ == "__main__":
#     pusher = PushNoti("https://api.pushover.net/1/messages.json", "a4povykn4dvyx4abyrhiva7mha73yu", "ucoahs1383n8vghor5pe6w3d5x2jre", "iphone", 0)
#     pusher.send_message()
