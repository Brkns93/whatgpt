import os
from dotenv import load_dotenv
from twilio_service import TwilioService
from openai_service import OpenAiService

class WpTwilioApp:
  def __init__(self):
    load_dotenv()
    self.conversations = self._load_conversations()
    try:
      self._config()
    except Exception as e:
      raise Exception("Could not configure application.")

  def _config(self):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    self.twilio_service = TwilioService(account_sid, auth_token)
    self.openai_service = OpenAiService()
  
  def _load_conversations(self) -> dict:
    return {}

  def _get_conversation(self, from_number: str, to_number: str) -> list:
    if f"{from_number}|{to_number}" in self.conversations:
      return self.conversations[f"{from_number}|{to_number}"]
    else:
      return []
  
  def process_message(self, from_number: str, twilio_number: str, incoming_message: str):
    user_id = from_number + "|" + twilio_number
    try:
      result = self.openai_service.chat(user_id, incoming_message)
      response = result.choices[0].message.content
      self.twilio_service.send_message(twilio_number, from_number, response)
    except Exception as e:
      self.twilio_service.send_message(twilio_number, from_number, "WpTwilio couldn't process your request.")
      print(e)
      