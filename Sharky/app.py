import cohere
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
co = cohere.Client('')

app = Flask(__name__)  
@app.route("/")
def index():    
    return render_template("index.html") 
@app.route("/get")
def get_bot_response():    
    txt = request.args.get('msg')    
    response = co.generate(
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
    print('Sharky: {}'.format(response.generations[0].text)) 
    reply=format(response.generations[0].text).strip("--")
    return str(reply) 
if __name__ == "__main__":    
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    app.run()

