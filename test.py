from notification.sms import SmsNotification


sms = SmsNotification(username="09038184873", default_from="50002710064873",
                      password="717d5b41-7432-4550-9682-dd2f41d16342")
result = sms.send(text = "salam agha mahyar", destination="09101612685")
print(result)
