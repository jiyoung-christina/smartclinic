#!/usr/bin/python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from SmartClinicServ import create_app
from flask.ext.socketio import SocketIO
from flask.ext.mail import Mail

import sys
reload(sys)

sys.setdefaultencoding("utf-8")

application = create_app()
application.config.update(
	        DEBUG=True,
	        #EMAIL SETTINGS
	        MAIL_SERVER='smtp.gmail.com',
	        MAIL_PORT=465,
	        MAIL_USE_SSL=True,
	        MAIL_USERNAME = 'ggamcong119@google.com',
	        MAIL_PASSWORD = 'qorwlgns119'
	    )
mail = Mail(application)
socketio = SocketIO(application)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    socketio.emit("response ", "socket com test")

if __name__ == '__main__':
     #application.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(application, host='0.0.0.0', port=5000)

