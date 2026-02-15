# from notification.sms import SmsNotification


# sms = SmsNotification(username="09038184873", default_from="50002710064873",
#                       password="717d5b41-7432-4550-9682-dd2f41d16342")
# result = sms.send(text = "salam agha mahyar", destination="09101612685")
# print(result)
import os
def find_resume_file(directory: str) -> str | None:
    for root, _, files in os.walk(directory):
        print(directory)
        for file in files:
            if file.lower().endswith(".pdf"):
                return os.path.join(root, file)
    return None


res = find_resume_file('./static')
print(res)