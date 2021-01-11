import json
from .. import models
from django.contrib.auth.models import User
from django.core.exceptions import *
from django.db import *
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus


@csrf_exempt
def users(request):
    if request.method == 'GET':
        return get_all_users()
    elif request.method == 'POST':
        return create_user(request)
    

def get_all_users():
    response = {'users': []}
    all_users = User.objects.all()

    for user in all_users:
        user_object = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        response['users'].append(user_object)

    return JsonResponse(data=response, status=HTTPStatus.OK)


def create_user(request):
    try:
        response = {}
        
        request_body = json.loads(request.body)
        first_name = request_body['first_name']
        last_name = request_body['last_name']
        username = request_body['username']
        password = request_body['password']

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        response['username'] = user.username
        response['first_name'] = user.first_name
        response['last_name'] = user.last_name
        response['email'] = user.email

        return JsonResponse(data=response, status=HTTPStatus.OK)

    except KeyError as e:
        return JsonResponse(data={'error': 'Invalid request payload'}, status=HTTPStatus.BAD_REQUEST)

    except IntegrityError as e:
        return JsonResponse(data={'error': 'User already exists.'}, status=HTTPStatus.CONFLICT)
