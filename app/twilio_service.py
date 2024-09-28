from twilio.rest import Client

class TwilioService:
  def __init__(self, account_sid: str, auth_token: str):
      try:
        self.client = Client(account_sid, auth_token)
      except:
        raise Exception("Twilio config is missing at least one of account_sid and auth_token")
      
  
  def send_message(self, from_phone: str, to_phone: str, message: str, media_url_addr: str=None):
    return_message = self.client.messages.create(
      from_=from_phone,
      to=to_phone,
      body=message,
      media_url=media_url_addr,
    )

    return return_message
