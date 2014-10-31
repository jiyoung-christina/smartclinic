# -*- coding: utf-8 -*-

from flask import Blueprint
from SmartClinicServ.SmartClinicLogger import Log

smartclinic = Blueprint('SmartClinicServ', __name__, template_folder='/Users/lacidjun/WebServer/SmartClinicServ/templates', static_folder='assets')

