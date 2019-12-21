from django.http import JsonResponse, Http404
import json

from django_sorcery.shortcuts import get_object_or_404

from userauth.models import User


def user_auth(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode("utf-8"))
        try:
            email = json_data['email']
            password = json_data['password']
            user = get_object_or_404(User, email=email)
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Please, provide both password and email.'}, status=500,
                                content_type="application/json")
        except Http404:
            return JsonResponse({'status': 'false', 'message': 'No such user.'}, status=404,
                                content_type="application/json")
        if not user.check_password(password):
            return JsonResponse({'status': 'false', 'message': 'Password is incorrect.'}, status=401,
                                content_type="application/json")
        token = user.get_jwt_token()
        data = {
            'pk': user.pk,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'middle_name': user.middle_name,
            'birth_data': user.birth_date,
            'nationality': user.nationality,
            'token': token,
        }
        return JsonResponse(data, content_type="application/json")
    return JsonResponse({'status': 'false', 'message': 'Only POST method is allowed.'}, status=405,
                        content_type="application/json")
