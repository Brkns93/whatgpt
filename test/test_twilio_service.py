import pytest
from os import getenv
from app.twilio_service import TwilioService

@pytest.fixture
def twilio_service():
  account_sid = getenv("TWILIO_ACCOUNT_SID")
  auth_token = getenv("TWILIO_AUTH_TOKEN")
  return TwilioService(account_sid, auth_token)

def test_send_message(twilio_service):
  try:
    twilio_service.send_message("whatsapp:+14155238886", "whatsapp:+31622044420", "Test message")
  except Exception as e:
    assert False, str(e)