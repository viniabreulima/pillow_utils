#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Collection of Pillow snippets
'''

import os
from PIL import Image

class PillowUtils(object):
    @staticmethod
    def resize_and_crop(src_img, dst_path=None, size=(100,100), crop_type='middle', save_params=[]):
        """
        Resize and crop an image to fit the specified size.

        args:
            img_path: path for the image to resize.
            modified_path: path to store the modified image.
            size: `(width, height)` tuple.
            crop_type: can be 'top', 'middle' or 'bottom', depending on this
                value, the image will cropped getting the 'top/left', 'middle' or
                'bottom/right' of the image to fit the size.
        raises:
            Exception: if can not open the file in img_path of there is problems
                to save the image.
            ValueError: if an invalid `crop_type` is provided.
        """
        if not crop_type in ('top', 'middle', 'bottom'):
            raise ValueError('invalid value for crop_type')

        if isinstance(src_img, Image.Image):
            img = src_img
        elif isinstance(src_img, str):
            img = Image.open(src_img)
        else:
            raise ValueError('invalid type for src_img')
        # If height is higher we resize vertically, if not we resize horizontally

        # Get current and desired ratio for the images
        img_ratio = img.size[0] / float(img.size[1])
        ratio = size[0] / float(size[1])
        
        #The image is scaled/cropped vertically or horizontally depending on the ratio
        if ratio > img_ratio:
            img = img.resize((size[0], round(size[0] * img.size[1] / img.size[0])),
                    Image.ANTIALIAS)
            # Crop in the top, middle or bottom
            if crop_type == 'top':
                box = (0, 0, img.size[0], size[1])
            elif crop_type == 'middle':
                box = (0, round((img.size[1] - size[1]) / 2), img.size[0],
                       round((img.size[1] + size[1]) / 2))
            elif crop_type == 'bottom':
                box = (0, img.size[1] - size[1], img.size[0], img.size[1])
                
            img = img.crop(box)
            
        elif ratio < img_ratio:
            img = img.resize((round(size[1] * img.size[0] / img.size[1]), size[1]),
                    Image.ANTIALIAS)
            # Crop in the top, middle or bottom
            if crop_type == 'top':
                box = (0, 0, size[0], img.size[1])
            elif crop_type == 'middle':
                box = (round((img.size[0] - size[0]) / 2), 0,
                       round((img.size[0] + size[0]) / 2), img.size[1])
            elif crop_type == 'bottom':
                box = (img.size[0] - size[0], 0, img.size[0], img.size[1])

            img = img.crop(box)
            
        else :
            # If the scale is the same, we do not need to crop
            img = img.resize((size[0], size[1]),
                    Image.ANTIALIAS)

        if dst_path:
            if not os.path.exists(os.path.dirname(dst_path)):
                os.makedirs(os.path.dirname(dst_path))
            img.save(*([dst_path] + save_params))
        return img


    def django_auto_resize_crop_rename(src_file, dst_prefix=None, size=(100,100),
                                       crop_type='middle', save_params=[],
                                       root_dir=''):
        '''
        '''

        img_name = src_file.name
        if img_name.startswith('./'):
            img_name = img_name[2:]
        dst_path = '{}@' + 'x'.join((str(x) for x in size)) + '.{}'
        url = os.path.join(dst_prefix, dst_path.format(*img_name.rsplit('.', 1)))
        if url.startswith('./'):
            url = url[2:]
        dst_path = os.path.join(root_dir, url)
        PillowUtils.resize_and_crop(src_img=str(src_file.file),
                                    dst_path=dst_path,
                                    size=size)
        return url
        
        
