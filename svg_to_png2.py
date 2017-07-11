import os
import cairosvg

from PIL import Image


def svg_to_png(path, img_name):
    target = os.path.abspath('static/')

    try:
        png_output = '{0}.png'.format(os.path.join(target,img_name).split(".")[0])
        cairosvg.svg2png(url=path, write_to=png_output)
        return png_output, 'png'

    except:
        output_path = os.path.join(target,img_name)
        os.rename(path, output_path)

        img = Image.open(output_path)
        img_format = img.format.lower()
        return output_path, img_format