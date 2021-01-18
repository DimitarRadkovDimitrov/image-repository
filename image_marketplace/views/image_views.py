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
        return JsonResponse(data={'error': 'User is not authenticated.'}, status=HTTPStatus.UNAUTHORIZED)


def get_images(request):
    response = {'images': []}
    all_public_images = models.Image.objects.exclude(is_private=True)

    for image in all_public_images:
        response['images'].append(model_to_dict(image))

    return JsonResponse(data=response, status=HTTPStatus.OK)


def upload_images(request):
    response = {}

    try:
        fire_storage = FireStorage()
        current_user = request.user
        image_files = request.FILES.getlist('images')
        image_metadata_list = json.loads(request.POST['meta'])
        response['images'] = []

        if len(image_files) != len(image_metadata_list):
            return JsonResponse(data={'error': 'Invalid request payload.'}, status=HTTPStatus.NOT_ACCEPTABLE)

        for i in range(len(image_files)):
            image_file = image_files[i].file
            image_metadata = image_metadata_list[i]

            storage_id = fire_storage.upload_file(image_file)
            new_image = store_image_data(current_user, image_metadata, storage_id)
            response['images'].append(model_to_dict(new_image))

        return JsonResponse(data=response, status=HTTPStatus.OK)

    except Exception as e:
        response['error'] = str(e)    
        return JsonResponse(data=response, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def delete_images(request):
    response = {}

    try:
        current_user = request.user
        request_body = json.loads(request.body)
        fire_storage = FireStorage()

        if "images" in request_body:
            for i in range(len(request_body['images'])):
                to_delete = models.Image.objects.get(pk=request_body['images'][i])

                if not _is_valid_deletion(current_user, to_delete):
                    return JsonResponse(
                        data={'error': 'User does not have access to this content.'},
                        status=HTTPStatus.FORBIDDEN
                    )   

                fire_storage.delete_file(to_delete.storage_id)
                delete_image_data(to_delete)
        else:
            to_delete = models.Image.objects.get(pk=request_body['id'])
            
            if not _is_valid_deletion(current_user, to_delete):
                return JsonResponse(
                    data={'error': 'User does not have access to this content.'},
                    status=HTTPStatus.FORBIDDEN
                )

            fire_storage.delete_file(to_delete.storage_id)
            delete_image_data(to_delete)

        return JsonResponse(data={}, status=HTTPStatus.OK)

    except ObjectDoesNotExist as e:
        return JsonResponse(
            data={'error': 'One or more of these images do not exist.'},
            status=HTTPStatus.BAD_REQUEST
        )

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


def delete_image_data(image):
    image.delete()


def _is_valid_deletion(user, image):
    if image.user != user:
        return False

    return True
