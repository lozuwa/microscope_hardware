from django.shortcuts import render

import re, json, io, base64, os
from PIL import Image
from random import randint

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage

from rest_framework.decorators import authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class ControllerView(APIView):
    def get(self, request, format=None):
        return render(request, 'PostMultiPartImage.html')

    def post(self, request, format=None):
        
        ''' Handle File '''
        file = request.FILES['file']
        fs = FileSystemStorage()
        _ = fs.save(file.name, file)

        
        return JsonResponse({'data': {'isClothe': True, 'classes': labels} })
