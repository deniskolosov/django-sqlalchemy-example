import json

from django.http import JsonResponse
from jose import jws, JWSError

from userauth.models import User


class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization').split(' ')[1]
            if 'password' in request.GET:
                password = request.GET['password']
                decoded_dict = {}
                try:
                    decoded_dict = json.loads(jws.verify(token, password, algorithms=['HS256']))
                except JWSError:
                    JsonResponse({'status': 'false', 'message': 'Token is incorrect'}, status=401,
                                 content_type="application/json")
                email = decoded_dict.get('email')
                user = User.objects.filter(email=email).scalar()
                if not user:
                    return JsonResponse({'status': 'false', 'message': 'User not found'}, status=401,
                                        content_type="application/json")
                request.custom_user = user
        response = self.get_response(request)
        return response
