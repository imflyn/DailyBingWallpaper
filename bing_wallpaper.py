import json
import os
import shutil
import time
import win32api
import win32gui

import requests
import win32con

URL = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
FILE_PATH = os.path.join(os.path.expanduser('~'), 'Desktop')


def set_wallpaper_from_bmp(bmp_path):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmp_path, win32con.SPIF_SENDWININICHANGE)


response = requests.get(URL).text
json_data = json.loads(response)
image_url = json_data['images'][0]['url']
if 'http' not in image_url:
    image_url = 'http://www.bing.com' + image_url
name = 'bing' + time.strftime('%Y%m%d', time.localtime(time.time())) + '.jpg'

response = requests.get(image_url, stream=True)
with open(FILE_PATH + '\\' + name, 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
set_wallpaper_from_bmp(FILE_PATH + '\\' + name)
