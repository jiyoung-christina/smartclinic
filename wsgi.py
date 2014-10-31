#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from SmartClinicServ import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)