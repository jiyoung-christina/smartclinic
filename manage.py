#!/usr/bin/python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from SmartClinicServ import create_app
from flask.ext.socketio import SocketIO
import sys
reload(sys)

sys.setdefaultencoding("utf-8")

application = create_app()
socketio = SocketIO(application)
if __name__ == '__main__':
    #application.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(application)

@socketio.on('message')
def handle_message(message):
    print 'test socketio'
    print('received message: ' + message)
