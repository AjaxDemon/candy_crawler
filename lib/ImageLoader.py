# coding: utf-8

import os
import requests
from lib.Logger import Logger
from requests import exceptions
from lib.FileHelper import write_file


class ImageLoader:

    ALLOWED_TYPES = ['image/png', 'image/jpg', 'image/jpeg']

    @staticmethod
    def grab(path, image_url, file_name=None):
        try:
            if not file_name:
                file_name = image_url.split('/')[-1]
            response = requests.get(image_url)
            content_type = response.headers['content-type']

            if content_type not in ImageLoader.ALLOWED_TYPES:
                return False
            prefix = content_type.split('/')[-1]
            file_name = '%s.%s' % (file_name, prefix)
            file_path = os.path.join(path, file_name)

            write_file(file_path, response.content)
        except exceptions.RequestException as error:
            Logger.record_log('Occurred Exception:', error)

