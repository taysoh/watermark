# -*- coding: utf-8 -*-
from rest_framework import serializers


class WatermarkSerializer(serializers.Serializer):
    order_hash = serializers.CharField(max_length=32, allow_blank=False, required=True)
    url = serializers.URLField(allow_blank=False, required=True)

    def validate_url(self, value):
        """
        Check that link on epub file
        """
        if '.epub' in value and value.index('.epub') == (len(value)-5): #len of '.epub' + index start fron 0
            return value
        else:
            raise serializers.ValidationError("Link should be on epub file")
