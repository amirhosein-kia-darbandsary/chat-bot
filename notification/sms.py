from melipayamak import Api
from notification.base import Notification


class SmsNotification(Notification):

    def __init__(self, username: str, password: str, default_from: str):
        self.username = username
        self.password = password
        self.default_from = default_from

        self.api = Api(self.username, self.password)
        self.sms = self.api.sms()

    def send(self, text: str, destination: str):
        try:
            response = self.sms.send(
                destination,
                self.default_from,
                text
            )
            print(response)
            return {
                "success": True,
                "response": response
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
