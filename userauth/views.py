from django.http import JsonResponse
import json


from userauth.models import User


def get_user_data(user, token):
    return {
            'pk': user.pk,
            'first_name': user.name,
            'last_name': user.last_name,
            'middle_name': user.middle_name,
            'birth_date': user.birth_date,
            'nationality': user.nationality.name.name,
            'token': token,
        }


def user_auth(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode("utf-8"))
        try:
            email = json_data['email']
            password = json_data['password']
            user = User.objects.filter(email=email).one_or_none()
            if not user:
                return JsonResponse({'status': 'false', 'message': 'No such user.'}, status=404,
                                    content_type="application/json")
        except KeyError:
            return JsonResponse({'status': 'false', 'message': 'Please, provide both password and email.'}, status=500,
                                content_type="application/json")
        if not user.check_password(password):
            return JsonResponse({'status': 'false', 'message': 'Password is incorrect.'}, status=401,
                                content_type='application/json')
        token = user.get_jwt_token(user_email=email, password=password)
        data = get_user_data(user, token)
        return JsonResponse(data, content_type='application/json')
    return JsonResponse({'status': 'false', 'message': 'Only POST method is allowed.'}, status=405,
                        content_type='application/json')


def profile(request):
    if request.method == 'GET':
        if getattr(request, 'custom_user', None):
            data = get_user_data(user=request.custom_user, token=request.custom_user.token)
            return JsonResponse(data, content_type="application/json")
        else:
            return JsonResponse({'status': 'false', 'message': 'User is not authorized.'}, status=401,
                                content_type='application/json')
    return JsonResponse({'status': 'false', 'message': 'Only GET method is allowed.'}, status=405,
                        content_type='application/json')


