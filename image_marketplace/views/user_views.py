import json
from .. import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import *
from django.db import *
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from http import HTTPStatus


def users(request):
    if request.method == 'GET':
        return get_all_users()

    elif request.method == 'POST':
        return create_user(request)


def get_all_users():
    response = {'users': []}
    all_users = User.objects.all()

    for user in all_users:
        response['users'].append(model_to_dict(user))

    return JsonResponse(data=response, status=HTTPStatus.OK)


def create_user(request):
    try:        
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

        response = model_to_dict(user)
        return JsonResponse(data=response, status=HTTPStatus.OK)

    except IntegrityError as e:
        return JsonResponse(data={'error': 'User already exists.'}, status=HTTPStatus.CONFLICT)
    
    except:
        return JsonResponse(data={'error': 'Invalid request payload'}, status=HTTPStatus.BAD_REQUEST)


def user_login(request):
    if request.method == 'POST':
        try:        
            request_body = json.loads(request.body)

            username = request_body['username']
            password = request_body['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                response = model_to_dict(user)
                return JsonResponse(data=response, status=HTTPStatus.OK)
            else:
                return JsonResponse(data={'error': 'Username or password incorrect.'}, status=HTTPStatus.NOT_ACCEPTABLE)
    
        except:
            return JsonResponse(data={'error': 'Invalid request payload.'}, status=HTTPStatus.BAD_REQUEST)
    else:
        return JsonResponse(data={'error': 'Method not allowed.'}, status=HTTPStatus.METHOD_NOT_ALLOWED)


def user_logout(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={'error': 'User is not authenticated.'}, status=HTTPStatus.UNAUTHORIZED)
    
    logout(request)
    return JsonResponse(data={'status': 'User successfully logged out.'}, status=HTTPStatus.OK)
