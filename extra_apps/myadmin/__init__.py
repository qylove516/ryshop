from django.utils.module_loading import autodiscover_modules


# 配置文件应该使用单例模式

def autodiscover():
    autodiscover_modules('myadmin')
