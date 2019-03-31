from django.contrib import messages
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from goods import models
from goods import goods_serializers
import json
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class GoodsAPIView(APIView):
    # authentication_classes = []

    def get(self, request, *args, **kwargs):
        goods_obj = models.Goods.objects.all()
        goods_ser = goods_serializers.GoodsSerializers(instance=goods_obj, many=True, context={'request': request})
        data = goods_ser.data
        # data = json.dumps(data, ensure_ascii=False)
        return Response(data)

    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response(1233123)


class PriceAPIView(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        return Response(pk)


####################################分页##################################
from rest_framework.pagination import PageNumberPagination


# 自定义PageNumberPagination
class MyPageNumberPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'size'
    max_page_size = 5

    page_query_param = 'page'


class PageGoodView(APIView):

    def get(self, request, *args, **kwargs):
        goods_obj = models.Goods.objects.all()
        pg = MyPageNumberPagination()
        pg_ser = pg.paginate_queryset(queryset=goods_obj, request=request, view=self)
        goods_ser = goods_serializers.GoodsSerializers(instance=pg_ser, many=True, context={'request': request})
        return pg.get_paginated_response(goods_ser.data)
        # return Response(goods_ser.data)


from rest_framework.viewsets import GenericViewSet
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


class GoodAutoAPIView(GenericViewSet):
    renderer_classes = [JSONRenderer, ]  # 返回的是json串
    pass


#################################一个model添加多张图片##################################
from goods.models import Images
from goods.forms import ImageForm, PostForm


def post(request):
    ImageFormSet = modelformset_factory(
        Images,
        form=ImageForm,
        fields=('id',),
        can_delete=True,
        extra=3,
        max_num=5
    )

    if request.method == 'POST':

        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = Images(post=post_form, image=image)
                photo.save()
            messages.success(request,
                             "Posted!")
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors, formset.errors)
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'index.html', {'postForm': postForm, 'formset': formset})


############################## 模板上传图片######################################
from django.shortcuts import render, HttpResponse
import os, json

def test(request):
    return render(request, 'images.html')


def upload_avatar(request):
    file_obj = request.FILES.get('avatar')
    file_path = os.path.join('static/images', file_obj.name)
    print(123)
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    return HttpResponse(file_path)


from django.core.cache import cache
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
import uuid


def bootstrap(request, *args, **kwargs):
    if request.method == "GET":
        # return render(request, 'bootstrap_file_input.html')
        images = models.ImageBootstrap.objects.all()
        # return render(request, 'new_bootstrap_file.html', {'images': images})
        return render(request, 'new_bootstrap_file.html', {'images': images})
    else:
        print('--------开始接收数据--------')
        images = request.FILES.getlist('file_data')
        ret = {
            'error': None,
        }
        image_id = []
        for image in images:
            image_data = [image.file, image.field_name, image.name, image.content_type,
                          image.size, image.charset, image.content_type_extra]
            cache_key = 'image_key'
            cache.set(cache_key, image_data, 60)

            cache_data = cache.get(cache_key)
            image = InMemoryUploadedFile(*cache_data)
            index = str(uuid.uuid4())
            models.ImageBootstrap(image=image, id=index).save()
            image_id.append(index)
        ret['image_id'] = "*".join(image_id)
        print(ret)
        return JsonResponse(ret)
