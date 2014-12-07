__author__ = 'lacidjun'
# -*- coding: utf-8 -*-

from flask import render_template, request, current_app, session, redirect, url_for
from functools import wraps
from werkzeug import check_password_hash

from SmartClinicServ.database import dao
from SmartClinicServ.SmartClinicLogger import Log
from SmartClinicServ.SmartClinicBlueprint import smartclinic



