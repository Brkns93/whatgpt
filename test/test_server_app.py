import pytest
from app.server_app import app

@pytest.fixture
def client():
  app.config["TESTING"] = True
  with app.test_client() as client:
    yield client

def test_home_endpoint(client):
  response = client.post("/twilio-webhook", data={
    "MessageSid": "test_sid",
    "From": "whatsapp:+31622044420",
    "To": "whatsapp:+14155238886",
    "Body": "Hello!"
  })
  assert response.status_code == 200
