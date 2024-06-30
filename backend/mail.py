from twilio.rest import Client

account_sid = 'AC28a231db44556c275f0d8e6f0823f2e7'
auth_token = '682024555c9d8bd1307c4f73da356593'

client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+13344535618',
  body='your 8th semester examination Date 15/04/2024 and Time 11:00 Am',
  to='+916377688671'
)

print(message.sid)