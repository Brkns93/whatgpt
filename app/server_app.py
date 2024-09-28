from flask import Flask, request
from wp_twilio_app import WpTwilioApp

app = Flask(__name__)

@app.route('/twilio-webhook', methods=['POST'])
def webhook():
  try:
    # Get the request data
    data = request.form

    # Extract the relevant information from the request
    message_sid = data.get('MessageSid')
    from_number = data.get('From')
    twilio_number = data.get('To')
    body = data.get('Body')

    print(f"Message SID: {message_sid}")
    print(f"From: {from_number}")
    print(f"To: {twilio_number}")
    print(f"Body: {body}")

    wp_twilio_app.process_message(from_number, twilio_number, body)

    # Respond to Twilio with an empty 200 OK response
    return "", 200
  except Exception as e:
    print(e)
    return "", 500

if __name__ == "__main__":
  wp_twilio_app = WpTwilioApp()
  app.run(host='0.0.0.0', port='8080')
