import json
from .. import models
from ..firestore import FireStorage
from django.contrib.auth.models import User
from django.core.exceptions import *
from django.db import *
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from http import HTTPStatus


def images(request):
    if request.method == 'GET':
        return get_images(request)
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return upload_images(request)  
        elif request.method == 'DELETE':
            return delete_images(request)
    else:
        return JsonResponse(data={'error': 'User is not authenticated.'}, status=HTTPStatus.NOT_ACCEPTABLE)


def get_images(request):
    response = {'images': []}
    all_public_images = models.Image.objects.exclude(is_private=True)

    for image in all_public_images:
        response['images'].append(model_to_dict(image))

    return JsonResponse(data=response, status=HTTPStatus.OK)


def upload_images(request):
    response = {}
    
    try:
        current_user = request.user
        request_body = json.loads(request.body)
        fire_storage = FireStorage()

        if "images" in request_body:
            response['images'] = []
            storage_ids = fire_storage.upload_files(request_body['images'])
            
            for i in range(len(request_body['images'])):
                new_image = store_image_data(current_user, request_body['images'][i], storage_ids[i])
                response['images'].append(model_to_dict(new_image))
        else:
            storage_id = fire_storage.upload_file(request_body)
            new_image = store_image_data(current_user, request_body, storage_id)
            response = model_to_dict(new_image)

        return JsonResponse(data=response, status=HTTPStatus.OK)

    except Exception as e:
        response['error'] = str(e)    
        return JsonResponse(data=response, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def delete_images(request):
    response = {}

    try:
        request_body = json.loads(request.body)
        fire_storage = FireStorage()

        if "images" in request_body:
            fire_storage.delete_files(request_body['images'])
        else:
            fire_storage.delete_file(request_body['id'])

        return JsonResponse(data={}, status=HTTPStatus.OK)

    except Exception as e:
        response['error'] = str(e)    
        return JsonResponse(data=response, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    

def store_image_data(user, image_record, storage_id):
    new_image = models.Image(
        user=user,
        title=image_record['title'],
        description=image_record['description'],
        is_private=image_record['is_private'],
        storage_id=storage_id,
        height=image_record['height'],
        width=image_record['width']
    )

    new_image.save()
    return new_image
