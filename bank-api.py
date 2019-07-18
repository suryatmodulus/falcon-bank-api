import os
import json
import logging
from wsgiref import simple_server
import falcon
from models import *
from playhouse.shortcuts import model_to_dict

class AuthMiddleware:

    def process_request(self, req, resp):
        token = req.get_header('Authorization')
        account_id = req.get_header('Account-ID')

        challenges = ['Token type="Fernet"']

        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized('Auth token required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')

        if not self._token_is_valid(token, account_id):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')

    def _token_is_valid(self, token, account_id):
        return True  # Suuuuuure it's valid...


class RequireJSON:

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')

class GetBankDetails:

    def __init__(self):
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp):
        ifsc = req.get_param('ifsc') or ''
        try:
            result =  model_to_dict(Branches.select().where(Branches.ifsc == ifsc.upper()).get())
        except Exception as ex:
            self.logger.error(ex)
            raise falcon.HTTPServiceUnavailable(
                'Service Outage',
                30)

        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result,indent=4, sort_keys=True)


class GetBranchDetails:
    def __init__(self):
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp):
        bank_name = req.get_param('bank_name') or ''
        city = req.get_param('city') or ''
        offset = req.get_param_as_int('offset') or 0
        limit = req.get_param_as_int('limit') or 0
        try:
            result = list(model_to_dict(branch) for branch in Branches.select().join(Banks).where(Banks.name == bank_name.upper(), Branches.city==city.upper()).offset(offset).limit(limit))
        except Exception as ex:
            self.logger.error(ex)
            raise falcon.HTTPServiceUnavailable(
                'Service Outage',
                30)

        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result,indent=4, sort_keys=True)

# Configure your WSGI server to load "things.app" (app is a WSGI callable)
# app = falcon.API(middleware=[
#     AuthMiddleware(),
#     RequireJSON(),
#     JSONTranslator(),
# ])

app = falcon.API()
app.add_route('/api/getBankDetails', GetBankDetails())
app.add_route('/api/getBranchDetails', GetBranchDetails())


if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 4000, app)
    print("Server started @ port 4000")
    httpd.serve_forever()

# IFSC - BARB0MITHAP
# Bank - BANK OF BARODA,MITHAPUR