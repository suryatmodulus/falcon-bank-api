import json
import logging
from wsgiref import simple_server
import falcon
from models import *
from playhouse.shortcuts import model_to_dict
import jwt
from datetime import datetime,timedelta

JWT_SECRET = "COFFEE"

EMAIL = "modulus@helloworld.in"
PASS = "foobar"



def jwtAuth(req,resp,resource,params):
    
    token = req.get_header('Authorization')
    if token is None:
        description = ('Please provide an auth token '
                       'as part of the request.')

        raise falcon.HTTPUnauthorized('Authentication Error',
                                      description)
    if not _token_is_valid(token):
        description = ('The auth token is invalid or has expired. '
                       'Please request a new token and try again.')

        raise falcon.HTTPUnauthorized('Authentication Token Error',
                                      description)

def _token_is_valid(token):
    try:
        payload = jwt.decode(token.split(" ")[1], JWT_SECRET, algorithms='HS256')
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False

class RedirectToGithub:

    def __init__(self):
        self.logger = logging.getLogger('bank-api-redirectToGithub' + __name__)

    def on_get(self, req, resp):
            resp.set_header("Powered-By","Falcon")
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({'status' : 'OK', 'API-DOCS-LINK' : 'https://github.com/suryatmodulus/falcon-bank-api/blob/master/README.md'})

class GetToken:

    def __init__(self):
        self.logger = logging.getLogger('bank-api-getToken' + __name__)

    def on_get(self, req, resp):
            raise falcon.HTTPBadRequest(
                'Request Method Error',
                'getToken excepts POST Request')

    def on_post(self, req, resp):
        email = req.get_param('email') or ''
        password = req.get_param('password') or ''
        raw = req.get_param('raw') or ''
        print(email,password)
        if(email==EMAIL and password==PASS):
            payload = {'email': EMAIL, 'exp': datetime.utcnow() + timedelta(days=5)}
            jwt_token = jwt.encode(payload, JWT_SECRET, algorithm='HS256').decode('utf-8')
            result = {"auth": "OK", "token" : jwt_token}
            resp.set_header("Powered-By","Falcon")
            resp.status = falcon.HTTP_200
            if(not raw=='' and raw=="true"):
                resp.body = jwt_token
            else:
                resp.body = json.dumps(result,indent=4, sort_keys=True)
        else:
            description = ('Make sure your email and password are correct.')
            raise falcon.HTTPUnauthorized('Incorrect Authentication Credentials',
                                          description)


class GetBankDetails:

    def __init__(self):
        self.logger = logging.getLogger('bank-api-getBankDetails' + __name__)

    @falcon.before(jwtAuth)
    def on_get(self, req, resp):
        ifsc = req.get_param('ifsc') or ''
        offset = req.get_param_as_int('offset') or 0
        limit = req.get_param_as_int('limit') or 0
        if(ifsc==''):
            raise falcon.HTTPMissingParam('ifsc')
        try:
            result =  model_to_dict(Branches.select().where(Branches.ifsc == ifsc.upper()).offset(offset).limit(limit).get())
        except Exception as ex:
            self.logger.error(ex)
            raise falcon.HTTPServiceUnavailable('Resource Not Found','Server was unable to fetch the requested data.')

        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result,indent=4, sort_keys=True)



class GetBranchDetails:

    def __init__(self):
        self.logger = logging.getLogger('bank-api-getBranchDetails' + __name__)

    @falcon.before(jwtAuth)
    def on_get(self, req, resp):
        bank_name = req.get_param('bank_name') or ''
        city = req.get_param('city') or ''
        offset = req.get_param_as_int('offset') or 0
        limit = req.get_param_as_int('limit') or 0
        if(bank_name=='' or city==''):
            raise falcon.HTTPMissingParam('bank_name and city')
        try:
            result = list(model_to_dict(branch) for branch in Branches.select().join(Banks).where(Banks.name == bank_name.upper(), Branches.city==city.upper()).offset(offset).limit(limit))
            if not result:
            	raise falcon.HTTPServiceUnavailable('Resource Not Found','Server was unable to fetch the requested data.')

        except Exception as ex:
            self.logger.error(ex)
            raise falcon.HTTPServiceUnavailable('Resource Not Found','Server was unable to fetch the requested data.')


        resp.set_header('Powered-By', 'Falcon')
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result,indent=4, sort_keys=True)


# Configure your WSGI server to load "things.app" (app is a WSGI callable)

app = falcon.API()
app.add_route('/',RedirectToGithub())
app.add_route('/api',RedirectToGithub())
app.add_route('/api/getToken', GetToken())
app.add_route('/api/getBankDetails', GetBankDetails())
app.add_route('/api/getBranchDetails', GetBranchDetails())


if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 4000, app)
    print("Server started @ port 4000")
    httpd.serve_forever()

# IFSC - BARB0MITHAP
# Bank - BANK OF BARODA,CHENNAI