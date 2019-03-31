"""ryshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import xadmin
from django.shortcuts import HttpResponse

"""
def func_1(request):
    return HttpResponse('func_1')


def func_2(request):
    return HttpResponse('func_2')


def func_3(request):
    return HttpResponse('func_3')


def list_view(request):
    return HttpResponse('list_views')


def add(request):
    return HttpResponse('add')


def change(request, id):
    return HttpResponse('change')


def delete(request, id):
    return HttpResponse('delete')
"""

"""
from goods import models
goods = models.Goods
type(goods)
<class 'django.db.models.base.ModelBase'>
goods._meta.model_name   #  得出model的名字
'goods'
goods._meta.app_label    # 得出app的名字
"""

"""
def get_second_urls():
    tmp = []
    tmp.append(path('list_views/', list_view))
    tmp.append(path('add/', add))
    tmp.append(re_path(r'^(\d+)/change/', change))
    tmp.append(re_path(r'^(\d+)/delete/', delete))
    return tmp


def get_urls():
    tmp = []
    for model, model_class_obj in admin.site._registry.items():
        app_name = model._meta.app_label
        model_name = model._meta.model_name
        tmp.append(path('{0}/{1}/'.format(app_name, model_name), (get_second_urls(), None, None)))
    return tmp
"""


from myadmin.service import myadmin
from django.views.static import serve
from ryshop import settings
from goods import views
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodAutoAPIView
from rest_framework import routers
router = routers.DefaultRouter


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('admin/', admin.site.urls),
    path('myadmin/', myadmin.site.urls),
    re_path('media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('api/', include('goods.urls')),
    path('user/', include('users.urls')),
    path('jwt/', obtain_jwt_token),
    # path('xmyadmin/', ([
    #                        path('func_1/', func_1),
    #                        path('func_2/', func_2),
    #                        path('func_3/', func_3),
    #                    ], None, None)),
    # path('myadmin/', (get_urls(), None, None))
]
