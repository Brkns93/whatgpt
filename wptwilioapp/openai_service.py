from openai import OpenAI, NotGiven
import base64
from typing import List, Dict, Any, Optional
import json

class OpenAiService:
  def __init__(self):
    # OpenAI client gets the API key from the environment variable OPENAI_API_KEYSSSS
    self.openai_client = OpenAI()
    self.sessions = {}
    self.tools = NotGiven()
    self.function_map = {}

  def _get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
    if session_id not in self.sessions:
      self.sessions[session_id] = []
    return self.sessions[session_id]
  
  def assign_tools(self, tools: List[Dict[str, Any]]):
    self.tools = [tool["tool_definition"] for tool in tools]
    self.function_map = {tool["tool_definition"]["function"]["name"]: tool["tool_method"] for tool in tools}

  def add_message(self, session_id: str, message: Dict[str, Any]):
    self._get_conversation_history(session_id).append(message)

  def encode_image(self, image_path: str) -> str:
    with open(image_path, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

  def chat_completion(self, session_id: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens: int = 150) -> Dict[str, Any]:
    messages = self._get_conversation_history(session_id).copy()
    try:
      response = self.openai_client.chat.completions.create(
        model=model,
        messages=messages,
        tools=self.tools,
        temperature=temperature,
        max_tokens=max_tokens,
        user=session_id
      )
    except Exception as e:
      print(e)
      response = None

    return response

  def process_response(self, session_id: str, response: Dict[str, Any]):
    choice = response.choices[0]
    
    if choice.finish_reason == "tool_calls":
      for tool_call in choice.message.tool_calls:
        message = choice.message
        self.add_message(session_id, message)
        function = tool_call.function
        function_name = function.name
        function_parameters = function.arguments

        # TODO: Handle the exceptions and return proper error messages
        function_to_call = self.function_map[function_name]

        method_args = list(json.loads(function_parameters).values())
        function_response = function_to_call(*method_args)
        function_call_result_message = {
          "role": "tool",
          "content": json.dumps(function_response),
          "tool_call_id": tool_call.id
        }
        
        self.add_message(session_id, function_call_result_message)
        
      return self.chat_completion(session_id)
    else:
      return response

  def generate_image(self, prompt: str, size: str = "1024x1024", n: int = 1) -> List[str]:
    response = self.openai_client.images.generate(
      prompt=prompt,
      n=n,
      size=size
    )
    
    return [img.url for img in response.data]

  def analyze_image(self, image_path: str, prompt: str) -> str:
    base64_image = self.encode_image(image_path)
    
    response = self.openai_client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {
            "role": "user",
            "content": [
              {"type": "text", "text": prompt},
              {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ],
          }
      ],
      max_tokens=300,
    )
    
    return response.choices[0].message.content

  def chat(self, session_id: str, user_input: str, image_path: Optional[str] = None) -> str:
    msg = {
      "role": "user",
      "content": user_input
    }
    self.add_message(session_id, msg)
    response = self.chat_completion(session_id)
    result = self.process_response(session_id, response)
    self.add_message(session_id, result.choices[0].message)
    return result


# Example usage
if __name__ == "__main__":
  service = OpenAiService()
      
  def generate_image(prompt: str) -> List[str]:
    image_urls = service.generate_image(prompt)
    if len(image_urls) > 0:
      image_url = image_urls[0]
      return {"image_url": image_url, "prompt": prompt}
    return {"image_url": "", "prompt": "No image could generated for the prompt."}
  
  tools = [
    {
      "tool_definition":{
        "type": "function",
        "function": {
          "name": "generate_image",
          "description": "Generate an image for a user's prompt. Call this whenever user wants to create a image using prompt, for example when a user asks 'A dreamy landscape with rolling hills, vibrant flowers, and a rainbow arcing across a clear blue sky.'",
          "parameters": {
            "type": "object",
            "properties": {
              "prompt": {
                "type": "string",
                "description": "User's prompt."
              }
            },
            "required": ["prompt"],
            "additionalProperties": False
          }
        }
      },
      "tool_method": generate_image
    }
  ]
  service.assign_tools(tools)
  
  # Chat example
  session_id = "session1"  # Example session ID
  while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
      break
    print("Assistant:", service.chat(session_id, user_input).choices[0].message.content)
