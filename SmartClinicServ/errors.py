#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import jsonify

def make_error(status_code, error_code, message):
    response = jsonify({'error': {'code':error_code, 'message':message}})
    response.status_code = status_code
    return response

def response_error(error_code):
    if error_code == 1000:
        return make_error(status_code=400, error_code=error_code, message='Not Exited User Id')
    elif error_code == 1001:
        return make_error(status_code=400, error_code=error_code, message='Aleady Exited User Id')
    elif error_code == 2000:
        return make_error(status_code=500, error_code=error_code, message='DB Insert Error')
    elif error_code == 3000:
        return make_error(status_code=400, error_code=error_code, message='Bad Request: Wrong Input Parameter')
    else:   #9999
        return make_error(status_code=400, error_code=error_code, message='Unknown Error')


class UserError(Exception):
    def __init__(self, status_code, error_code, message):
        Exception.__init__(self)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message

    def to_dict(self):
        rv = {'error': {'code':self.error_code, 'message':self.message}}
        return rv