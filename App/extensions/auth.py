import jwt
import datetime
from jwt import exceptions
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, JsonResponse

SALT = settings.SECRET_KEY


def create_token(payload, timeout=20):

    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    token = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)
    return token

class JwtQueryParamMiddleware(MiddlewareMixin):

    def process_request(self,request):
        if request.path_info == '/loginJWT/':
            return
        token = request.GET.get('token')
        try:
            verified_payload = jwt.decode(token, SALT,algorithms=['HS256'])
            request.jwt_payload = verified_payload
        except exceptions.ExpiredSignatureError:
            return JsonResponse({'error':'token已失效'})
            raise
        except jwt.DecodeError:
            return JsonResponse({'error':'token认证失败'})
            raise
        except jwt.InvalidTokenError:
            return JsonResponse({'error':'非法的token'})
            raise
        return None
