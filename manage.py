#!/usr/bin/python
# -*- coding: utf-8 -*-
from SmartClinicServ import create_app
import sys
reload(sys)

sys.setdefaultencoding("utf-8")

application = create_app()

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=True)

