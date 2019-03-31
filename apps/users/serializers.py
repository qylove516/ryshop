from rest_framework import serializers
from rest_framework_jwt.compat import Serializer


class JWTserializer(Serializer):

    def __init__(self, *args, **kwargs):
        super(JWTserializer, self).__init__(*args, **kwargs)
        self.fields["tel"] = serializers.CharField()
