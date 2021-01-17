import json
from .. import models
from ..firestore import FireStorage
from django.contrib.auth.models import User
from django.core.exceptions import *
from django.db import *
from django.http import JsonResponse
from django.shortcuts import render
from http import HTTPStatus


def images(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={'error': 'User is not authenticated.'}, status=HTTPStatus.NOT_ACCEPTABLE)
 
    if request.method == 'POST':
        return upload_images(request)
        
    elif request.method == 'DELETE':
        return delete_images(request)


def upload_images(request):
    response = {}
    request_body = json.loads(request.body)
    fire_storage = FireStorage()

    try:
        if "images" in request_body:
            response['images'] = fire_storage.upload_files(request_body['images'])
        else:
            response['id'] = fire_storage.upload_file(request_body)

        return JsonResponse(data=response, status=HTTPStatus.OK)

    except Exception as e:
        response['error'] = str(e)    
        return JsonResponse(data=response, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def delete_images(request):
    response = {}
    request_body = json.loads(request.body)
    fire_storage = FireStorage()

    try:
        if "images" in request_body:
            fire_storage.delete_files(request_body['images'])
        else:
            fire_storage.delete_file(request_body['id'])

        return JsonResponse(data={}, status=HTTPStatus.OK)

    except Exception as e:
        response['error'] = str(e)    
        return JsonResponse(data=response, status=HTTPStatus.INTERNAL_SERVER_ERROR)
