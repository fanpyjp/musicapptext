import redis
import jwt
import datetime
from jwt import exceptions
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, JsonResponse

SALT = settings.SECRET_KEY

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def create_token(payload, timeout=20):

    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    user_id = payload['userid']
    struser_id = f'userid:{user_id}'
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    token = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)
    redis_ms = redis_client.setex(name=struser_id, time=timeout * 60, value=token)
    print(redis_ms)
    return token

class JwtQueryParamMiddleware(MiddlewareMixin):

    def process_request(self,request):
        if request.path_info == '/loginJWT/':
            return
        token = request.GET.get('token')
        try:
            verified_payload = jwt.decode(token, SALT,algorithms=['HS256'])
            request.jwt_payload = verified_payload
            user_id = verified_payload.get('userid')
        except exceptions.ExpiredSignatureError:
            return JsonResponse({'error':'token已失效'})
            raise
        except jwt.DecodeError:
            return JsonResponse({'error':'token认证失败'})
            raise
        except jwt.InvalidTokenError:
            return JsonResponse({'error':'非法的token'})
            raise
        redis_key = f"userid:{user_id}"
        print(redis_key)
        redis_token = redis_client.get(redis_key)
        print(redis_token)
        if not redis_token or redis_token.decode('utf-8') != token:
            return JsonResponse({'error':'token认证失败'})
            raise
        return None
