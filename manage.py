#!/usr/bin/python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from SmartClinicServ import create_app

import sys
reload(sys)

sys.setdefaultencoding("utf-8")

application, socketio = create_app()

if __name__ == '__main__':
    #application.run(host='0.0.0.0', port=5000, debug=True)
    socketio.run(application)

@socketio.on('message')
def handle_message(message):
    print 'test socketio'
    print('received message: ' + message)
