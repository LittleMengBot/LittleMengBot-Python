# -*- coding: utf-8 -*
# 这是一个给图片添加水印的模块。
# pip3 install Pillow
from PIL import Image

def watermark(img_source, img_new) ->bool:
    img_water = "/xxx/xxx/xxx.png"    # 水印文件路径，最好填完整。
    try:
        source = Image.open(img_source).convert("RGBA")
        water = Image.open(img_water).convert("RGBA")
        i_x, i_y = source.size
        w_x, w_y = water.size
        base_wrate = w_x / w_y
        base_srate = i_x / i_y
        if i_x < 1280:    # 对于x小于1280像素的图片进行拉伸，防止水印模糊。
            source = source.resize((1280, int(1280 / base_srate)), Image.LANCZOS and Image.ANTIALIAS)
            i_x, i_y = source.size
        new_wx = int(i_x / 3.5)
        new_wy = int(new_wx / base_wrate)
        water = water.resize((new_wx, new_wy), Image.LANCZOS and Image.ANTIALIAS)
        layer = Image.new('RGBA', source.size, (0, 0, 0, 0))
        layer.paste(water, (source.size[0] - new_wx, source.size[1] - new_wy))
        newIm = Image.composite(layer, source, layer)
        newIm.save(img_new)

    except Exception as e:
        print(">>>>>>>>>>> WaterMark EXCEPTION:  " + str(e))
        return False
    else:
        return True