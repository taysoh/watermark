from zipfile import ZipFile
from django.test import TestCase
from cStringIO import StringIO
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
import uuid
from datetime import datetime
import re
client = APIClient()


class CheckWatermark(TestCase):
    def test(self):
        """
        Check server response, file name and  order hash and timestamp applying
        """

        order_hash = uuid.uuid4().hex
        url = 'https://s3.eu-central-1.amazonaws.com/saxo-static/ebooks/line-vindernovelle-i-krimidysten.epub'

        response = client.get(reverse('add_mark')+'?url=%s&order_hash=%s' % (url, order_hash))
        origin_name = url.split('/')[-1]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn('filename=%s' % origin_name, response.get('Content-Disposition'))
        zipped_file = ZipFile(StringIO(response.content), 'r')

        file_to_check = 'META-INF/container.xml'
        # check only date because can be next hour after file received
        timestamp = datetime.now().strftime('%Y-%m-%d')

        self.assertIn(file_to_check, zipped_file.namelist())
        for item in zipped_file.infolist():
            if item.filename == file_to_check:
                data = zipped_file.read(item.filename)

                self.assertIn(order_hash, data)
                self.assertIn(timestamp, data)

        zipped_file.close()