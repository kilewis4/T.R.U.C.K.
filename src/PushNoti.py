import requests
import os

class PushNoti:
    """
    A class to send push notifications using the Pushover API.

    This class allows you to send notifications to a specific device through the Pushover API. 
    It sends messages containing information about the next door (or task) assigned.
    """
    def __init__(self, url, deviceName, door):
        """
        Initializes the PushNoti object with necessary parameters.

        Args:
            url (str): The Pushover API URL to send notifications to.
            deviceName (str): The device name to send the notification to.
            door (int): The door number that is part of the notification message.
        """
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
        """
        Sends the notification message to the specified device using the Pushover API.

        This method sends the POST request with the data defined in the `__init__` method 
        to the Pushover API and prints the response in JSON format.

        Returns:
            None
        """
        response = requests.post(self.PUSHOVER_API_URL, data=self.data)
        print(response.json())

# if __name__ == "__main__":
#     pusher = PushNoti("https://api.pushover.net/1/messages.json", "a4povykn4dvyx4abyrhiva7mha73yu", "ucoahs1383n8vghor5pe6w3d5x2jre", "iphone", 0)
#     pusher.send_message()
