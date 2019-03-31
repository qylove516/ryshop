from django.urls import path, re_path
from goods import views

urlpatterns = [
    path('', views.GoodsAPIView.as_view()),
    path('page/', views.PageGoodView.as_view()),
    re_path(r'price/(?P<pk>\d+)/', views.PriceAPIView.as_view(), name='price'),
    path('post_image/', views.post, name='qi'),
    path('upload_avatar/', views.upload_avatar),  # 上传头像
    path('test/', views.test),  # 测试页面
    path('bs4/', views.bootstrap, name='bs4'),
]