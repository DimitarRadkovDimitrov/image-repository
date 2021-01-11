import json
from .. import models
from ..firestore import FireStorage
from django.contrib.auth.models import User
from django.core.exceptions import *
from django.db import *
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from http import HTTPStatus


@csrf_exempt
def images(request):
    if request.method == 'POST':
        return upload_image(request)
    elif request.method == 'DELETE':
        return delete_image(request)


def upload_image(request):
    response = {}
    request_body = json.loads(request.body)

    image_file_path = request_body['image_file_path']
    image_metadata = request_body['metadata']
    
    fire_storage = FireStorage()

    try:
        created_id = fire_storage.upload_file(image_file_path, image_metadata)
        response['id'] = created_id
        return JsonResponse(data=response, status=HTTPStatus.OK)

    except Exception as e:
        response['error'] = str(e)    
        return JsonResponse(data=response, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def delete_image(request):
    response = {}
    request_body = json.loads(request.body)

    image_id = request_body['id']
    fire_storage = FireStorage()

    try:
        fire_storage.delete_file(image_id)
        return JsonResponse(data={}, status=HTTPStatus.OK)

    except Exception as e:
        response['error'] = str(e)    
        return JsonResponse(data=response, status=HTTPStatus.INTERNAL_SERVER_ERROR)
