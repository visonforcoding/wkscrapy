import json
import requests
import os
from fpdf import FPDF
import img2pdf
from PIL import Image
import sys
import coloredlogs
import logging
## 日志模块
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

# filePath = '2019汽配维修保养行业分析报告.har'
if len(sys.argv) > 1:
    filePath = sys.argv[1]
    print(filePath)
else:
    logger.error('错误的启动方式,未找到文件')
    sys.exit()
file_name = filePath.split('.')[0]
cwd = os.getcwd()
if os.path.exists(file_name) is not True:
    os.mkdir(file_name)
img_list = []
with open(filePath, 'r') as readObj:
    harDirct = json.loads(readObj.read())
    entriesList = harDirct['log']['entries']

    img_num = 1
    for entrie in entriesList:
        request = entrie['request']
        img_url = request['url']
        # 下载图片
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            png_name = "%s/%s/%s.png" % (cwd, file_name, img_num)
            with open(png_name, "wb") as png:
                png.write(r.content)
            img_list.append(png_name)
        img_num = img_num + 1

pdf_name = "%s.pdf" % file_name
im1 = Image.open(img_list[0])
img_list.pop(0)
new_pic = []
for i in img_list:
    img = Image.open(i)
    if img.mode == "RGBA":
        img = img.convert('RGB')
        new_pic.append(img)
    else:
        new_pic.append(img)
im1.save(pdf_name,
         "PDF",
         resolution=100.0,
         save_all=True,
         append_images=new_pic)

logger.info('文件生成%s' % pdf_name)
