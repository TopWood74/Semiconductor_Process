from django.shortcuts import render, redirect
import json
from django.http import JsonResponse

import urllib.request
from bs4 import BeautifulSoup
import urllib.parse

import program.scan as scan
import yolov5.detect_django as yolo

#https://axce.tistory.com/3
#from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import os

def scanimage(request):
    #print(settings.BASE_DIR, settings.MEDIA_ROOT, settings.MEDIA_URL)
    #print(str(settings.BASE_DIR))    
    context = {}
    return render(request, 'program/scanimage.html', context)

def scanimage_upload(request):
    if request.method == 'POST' and request.FILES.getlist('file'):
        #myfiles = request.FILES['file']
        myfiles = request.FILES.getlist('file')

        # print('myfiles: ', myfiles)

        filename_path = str(settings.BASE_DIR) + "/"

        location = '_media/screening_ab1'
        base_url = '/media/screening_ab1'
        img_path = filename_path + location + "/"
        # print("img_path", img_path)

        for f in os.listdir(img_path):
            os.remove(img_path + f)

        location2 = '_media/screening_ab2'
        base_url2 = '/media/screening_ab2'
        img_path2 = filename_path + location2 + "/"

        fs = FileSystemStorage(location=location, base_url=base_url)

        imgs = []
        for myfile in myfiles:
            # FileSystemStorage.save(file_name, file_content)
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            # print("filename:", uploaded_file_url)

            # img = base_url +"/" + scan.crop(location, filename)
            img = base_url +"/" + filename
            imgs.append(img)

        img_dic = yolo.yolo_image(img_path, img_path2)
        save_dir = img_dic['save_dir']
        img_tensor = img_dic['img_tensor']

        base_url2 = save_dir.replace("/mnt/c/Users/admin/workspace/web_project/_media/screening_ab2", base_url2)
        # print("base_url2:", base_url2)

        _filename = []
        _tenser = []
        for i, img in enumerate(img_tensor):
            _filename.append(base_url2 + "/" + img[0])

            if img[1] is None:
                _tenser.append(img[1])
            else:
                _tenser.append(img[1].tolist())                


            # print('_tenser:',_tenser)

        context = {"img" : _filename, "arr": _tenser}
    else:
        context = {"img": None, "arr": None}

    return JsonResponse(context)
