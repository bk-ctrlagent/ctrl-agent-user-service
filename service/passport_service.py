import os
from dotenv import load_dotenv
import jwt.exceptions
from werkzeug.exceptions import Unauthorized
from jwt import JWT
import jwt
load_dotenv()


class PassportService:
    def __init__(self):
        self.sk = jwt.jwk.OctetJWK(key=os.getenv('SECRET_KEY').encode('utf-8'))
    
    def issue(self, payload):
        jwt = JWT()
        return jwt.encode(payload, self.sk, alg='HS256')
    
    def verify(self, token):
        try:
            jwt = JWT()
            return jwt.decode(token, self.sk, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise Unauthorized('Invalid token signature.')
        except jwt.exceptions.DecodeError:
            raise Unauthorized('Invalid token.')
        except jwt.exceptions.ExpiredSignatureError:
            raise Unauthorized('Token has expired.')
