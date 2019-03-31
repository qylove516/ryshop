from django.test import TestCase


class Foo(object):
    _instance = None

    def __init__(self, name):
        self.name = name

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance


obj = Foo('Jhon')
obj2 = Foo('Mary')

print(id(obj), id(obj2))