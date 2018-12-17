# coding: utf-8

import os
from urllib.request import urlretrieve, HTTPError

class ImageLoader:
    """
	图片下载器
	"""

    @staticmethod
    def grab(path, image_url, file_name=None):
        try:
            if not file_name:
                file_name = image_url.split('/')[-1]
            file_path = os.path.join(path, file_name)
            urlretrieve(image_url, file_path)
        except HTTPError as e:
            print('Error: can not grab image, ', e)
