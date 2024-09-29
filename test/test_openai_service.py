import pytest
from app.openai_service import OpenAiService

@pytest.fixture
def openai_service():
  return OpenAiService()

def test_generate_text(openai_service):
  try:
    openai_service.chat("mock_session_id", "Hello!")
  except Exception as e:
    assert False, str(e)
