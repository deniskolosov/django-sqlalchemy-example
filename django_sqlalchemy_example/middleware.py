import json

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect

from userauth.models import User


class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "Authorization" in request.headers:
            token = request.headers.get('Authorization').split(' ')[1]
            data = json.loads(request.readlines()[0])
            user = User.objects.filter(email=data.get('email')).scalar()
            if not user:
                return JsonResponse({'status': 'false', 'message': 'No such t user.'}, status=404,
                                    content_type="application/json")
            if user.token != token:
                return JsonResponse({'status': 'false', 'message': 'Token is incorrect.'}, status=401,
                                    content_type="application/json")
            request.custom_user = user
        response = self.get_response(request)
        return response