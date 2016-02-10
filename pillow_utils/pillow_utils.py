#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Collection of Pillow snippets
'''

import os
from PIL import Image, ImageColor

class PillowUtils(object):
    @classmethod
    def resize_and_crop(cls, src_img, dst_path=None, size=(100,100), crop_type='middle', save_params=[]):
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

        img = cls.open_img(src_img)
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

        cls.save_img(dst_path, img, save_params)
        return img


    @classmethod
    def resize_and_fit(cls, src_img, dst_path=None, size=(100,100), fit_type='middle', fill_color='#000000', save_params=[]):
        """
        Resize and fit an image to fit the specified size.

        args:
            img_path: path for the image to resize.
            modified_path: path to store the modified image.
            size: `(width, height)` tuple.
            fit_type: can be 'top', 'middle' or 'bottom', depending on this
                value, the image will fitted getting the 'top/left', 'middle' or
                'bottom/right' of the image to fit the size.
        raises:
            Exception: if can not open the file in img_path of there is problems
                to save the image.
            ValueError: if an invalid `fit_type` is provided.
        """
        if not fit_type in ('top', 'middle', 'bottom'):
            raise ValueError('invalid value for crop_type')

        img = cls.open_img(src_img)

        # Get current and desired ratio for the images
        img_ratio = img.size[0] / float(img.size[1])
        ratio = size[0] / float(size[1])

        color = ImageColor.getrgb(fill_color)
        bg = Image.new(img.mode, size, color)

        paste_bg = True
        if ratio < img_ratio:
            img = img.resize((size[0], round(size[0] * img.size[1] / img.size[0])),
                    Image.ANTIALIAS)
        elif ratio > img_ratio:
            img = img.resize((round(size[1] * img.size[0] / img.size[1]), size[1]),
                    Image.ANTIALIAS)
        else :
            # If the scale is the same, just resize
            img = img.resize((size[0], size[1]),
                    Image.ANTIALIAS)
            paste_bg = False

        if paste_bg:
            pos = None
            if fit_type == 'top':
                pos = (0, 0)
            elif fit_type == 'middle':
                pos = (int((size[0] - img.size[0]) / 2), int((size[1] - img.size[1]) / 2))
            elif fit_type == 'bottom':
                pos = (size[0] - img.size[0], size[1] - img.size[1])
            bg.paste(img, pos)
            img = bg

        cls.save_img(dst_path, img, save_params)
        return img


    @classmethod
    def open_img(cls, src_img):
        if isinstance(src_img, Image.Image):
            return src_img
        elif isinstance(src_img, str):
            return Image.open(src_img)
        else:
            raise ValueError('invalid type for src_img')


    @classmethod
    def save_img(cls, dst_path, img, save_params=[]):
        if not dst_path:
            return
        fp = os.path.abspath(dst_path)
        fd = os.path.dirname(fp)
        if not os.path.exists(fd):
            os.makedirs(fd)
        return img.save(*([fp] + save_params))


    @classmethod
    def django_prepare(cls, src_file, dst_prefix, size, root_dir):
        img_name = src_file.name
        if img_name.startswith('./'):
            img_name = img_name[2:]
        dst_path = '{}@' + 'x'.join((str(x) for x in size)) + '.{}'
        url = os.path.join(dst_prefix, dst_path.format(*img_name.rsplit('.', 1)))
        if url.startswith('./'):
            url = url[2:]
        dst_path = os.path.join(root_dir, url)
        ret = os.path.isfile(dst_path)
        return ret, url, dst_path


    @classmethod
    def django_auto_resize_crop_rename(cls, src_file, dst_prefix=None,
                                       size=(100,100), crop_type='middle',
                                       save_params=[], root_dir=''):
        '''
        '''

        exists, url, dns_path = cls.django_prepare(src_file, dst_prefix, size, root_dir)
        if exists:
            return url
        try:
            cls.resize_and_crop(src_img=str(src_file.file), dst_path=dst_path,
                                crop_type=crop_type, size=size)
        except Exception as e:
            url = None
        return url


    @classmethod
    def django_auto_resize_fit_rename(cls, src_file, dst_prefix=None,
                                      size=(100,100), fit_type='middle',
                                      save_params=[], root_dir='',
                                      fill_color='#FFFFFF'):
        '''
        '''

        exists, url, dst_path = cls.django_prepare(src_file, dst_prefix, size, root_dir)
        if exists:
            return url
        try:
            cls.resize_and_fit(src_img=str(src_file.file), dst_path=dst_path,
                               fit_type=fit_type, size=size, fill_color=fill_color)
        except Exception as e:
            print(e)
            url = None
        return url


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Command line methods for PillowUtils')
    ap.add_argument('op', choices=('crop', 'fit'))
    ap.add_argument('src_img')
    ap.add_argument('dst_path')
    ap.add_argument('--size', nargs=2, type=int, default=(200, 200))
    ap.add_argument('--fit_type', choices=('top', 'middle', 'bottom'), default='middle')
    ap.add_argument('--fill_color', help='RGB(A) color: #RRGGBB or #RRGGBBAA')
    args = ap.parse_args()
    p = PillowUtils
    params = {
        'src_img': args.src_img,
        'dst_path': args.dst_path,
        'size': args.size,
    }
    if args.fill_color:
        params['fill_color'] = args.fill_color

    proc = None
    if args.op == 'crop':
        if args.fit_type:
            params['crop_type'] = args.fit_type
        proc = p.resize_and_crop
    elif args.op == 'fit':
        if args.fit_type:
            params['fit_type'] = args.fit_type
        proc = p.resize_and_fit


    proc(**params)
