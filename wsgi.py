#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from SmartClinicServ import create_app

import sys
reload(sys)

sys.setdefaultencoding("utf-8")

application, socketio = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(application, port=port)