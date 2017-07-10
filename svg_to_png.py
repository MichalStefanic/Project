import os
import cairosvg

def svg_to_png(path, img_name):
    target = os.path.abspath("static/")
    
    if not os.path.isdir(target):
        os.mkdir(target)

    try:
        png_output = os.path.join(target,img_name).split(".")[0]+".png"
        cairosvg.svg2png(
            url=path, write_to=png_output)
    except:
        output_path = os.path.join(target,img_name)
        os.rename(path, output_path)
