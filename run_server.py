from server.JPCServer import JPCServer
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import threading
import string
import os
import sys

app = Flask(__name__)
#app.config['DEBUG'] = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/Users/jameskraemer/Documents/JPC/server/gui/Uploads'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(os.path.join(app.instance_path, 'Uploads'), exist_ok=True)

path = os.path.dirname(__file__)
sys.path.append(path)


def run_server(server):
    server.run()


@app.route('/get_message', methods=['POST'])
def get_message():
    messageFromHTML = request.form['MessageBox']
    messageRecipient = request.form['chooseRecipient']
    try:
        messageImage = request.files['MessageImage']
    except:
        messageImage = None

    if messageImage :
        path = os.path.join(app.instance_path, 'Uploads', secure_filename(messageImage.filename))
        messageImage.save(path)
        server.send_image(path, messageRecipient)

    messages = []
    messageLog = open("messageLog.txt", "a")
    messageLog.write("To " + messageRecipient + ": " + messageFromHTML + "\n")

    server.send_message(messageFromHTML, messageRecipient)

    messagesFile = open("messageLog.txt", "r")
    for message in messagesFile:
            messages.append(message)

    messages.reverse()

    return render_template('index.html', messages=messages[0:10], firstMessage="To " + messageRecipient + ": " + messageFromHTML + "\n")


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    server = JPCServer()
    threading.Thread(target=run_server, args=[server]).start()
    app.run(port=5000)
