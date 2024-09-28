# WpTwilioApp
This project enables developers to integrate ChatGPT with WhatsApp using Twilio. It provides a seamless way to connect OpenAI's powerful language model with WhatsApp messaging, allowing for automated responses and interactions. This setup is intended for development purposes. For production deployment, please follow the Flask production guidelines.

## Dependencies
- You have to register for a WhatsApp phone number through Twilio, free tier includes a Sandbox. (https://www.twilio.com/docs/whatsapp/tutorial/requesting-access-to-whatsapp)
- After registiration you should configure webhook through settings. Enter http://{YOUR_PUBLIC_IP}/twilio-webhook to **"When a message comes in"** input.
- You have to get your OpenAI API key from the platform.

## Installation
You should configure the **.env** file before starting the application. Copy the **wptwilioapp/.env.config** file as **wptwilioapp/.env** and fill the secrets from Twilio and OpenAI. Pull this repo and run `install.sh`. This script will install necessary tools and start the application.  
Tested on Ubuntu 22.04.

## Deploy with AWS EC2
- Follow the instructions on the tutorial to launch an EC2 instance with **Ubuntu**: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html
- Connect your instance by following the instructions on https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-methods.html
After connecting your instance, use following commands to pull and start the project:
```bash
git pull https://github.com/Brkns93/whatgpt.git
cd whatgpt
./install.sh
```
- Use your public IPv4 DNS address as your Twilio sandbox webhook. E.g. http://aws-ec2.com/twilio-webhook
