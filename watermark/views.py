# -*- coding: utf-8 -*-
from urllib2 import urlopen
from datetime import datetime
from cStringIO import StringIO
from zipfile import ZipFile
import tempfile
import mimetypes

from django.http.response import HttpResponse


from .serializers import WatermarkSerializer
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework import status

import os


def add_hash(url, order_hash):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    input_file = ZipFile(StringIO(urlopen(url).read()), 'r')
    tempdir = tempfile.mkdtemp()

    file_name = url.split('/')[-1]
    file_path = os.path.join(tempdir, file_name)

    with ZipFile(file_path, 'w') as new_file:
        for epub_file in input_file.filelist:
            data = input_file.read(epub_file.filename)
            if epub_file.filename == 'META-INF/container.xml':
                data += '<!-- %s %s -->' % (order_hash, timestamp)
            new_file.writestr(epub_file, data)
    input_file.close()
    return file_path, file_name

class MarkView(RetrieveAPIView):
    serializer_class = WatermarkSerializer

    def get(self, request, *args, **kwargs):
        data = request.GET.copy()
        serializer = WatermarkSerializer(data=data)
        if serializer.is_valid():
            file_path, file_name = add_hash(**serializer.validated_data)
            response = HttpResponse(
                open(file_path, 'rb'),
                content_type=getattr(mimetypes, 'types_map', {}).get(os.path.splitext(file_name)[1])
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % file_name
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)