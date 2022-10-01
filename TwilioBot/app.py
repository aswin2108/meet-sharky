import cohere
from datetime import time
import re
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
co = cohere.Client('')


app = Flask(__name__)
def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if  len(incoming_msg)>0:
      txt=incoming_msg
      responsetxt = co.generate(
      model='large',
      prompt='Sharky is an Intelligent Shark Chatbot that spreads awareness about saving our oceans and answers questions regarding saving the enviroment\n\nMe: Hi\nSharky: Oceans are very polluted these days you can help it by cleaning the beaches\n--\nMe: What can I do to save the oceans?\nSharky: You can help ocean by helping to clean the beaches and avoid plastic as much as possible\n--\nMe: What do I do when I travel to a beach?\nSharky: You should avoid littering and carry your towels whenever you go to the beach\n--\nMe:{}\nSharky:'.format(txt), 
      max_tokens=50,
      temperature=0,
      k=0,
      p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop_sequences=["--"],
      return_likelihoods='NONE')
      message=format(responsetxt.generations[0].text).strip("--")
      msg.body(message)
      print('Sharky: {}'.format(responsetxt.generations[0].text))
    return str(resp)    

if __name__ == '__main__':
    app.run()






