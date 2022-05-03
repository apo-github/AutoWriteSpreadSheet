import webbrowser
import datetime
import subprocess
from subprocess import PIPE
import pyautogui as pg
import pyperclip
import time
import os
import sys


def get_ssid():  #SSID:無線LANの名前 #bssid:無線LANのMACアドレス
    ssid_info = subprocess.run("netsh wlan show interfaces",
                               shell=True,
                               stdout=PIPE,
                               stderr=PIPE,
                               text=True)
    datalist = ssid_info.stdout.split('\n')
    for data in datalist:
        if data.find('    SSID') == 0:
            ssid = data[data.find(':') + 2:len(data)]
            # print('ssid = ' + ssid)
        elif data.find('    BSSID') == 0:
            bssid = data[data.find(':') + 2:len(data)]
            # print('bssid = ' + bssid)

    return ssid


def file_read():
    f = open('keys.txt', 'r', encoding='UTF-8')
    datalist = f.readlines()
    row = str(datalist[0])
    url = str(datalist[1])
    ssid = str(datalist[2])
    return row, url, ssid


def get_col():
    dt_now = datetime.date.today()
    day = dt_now.strftime('%a')  # => 'Sun'
    col = 'D'
    if day == 'Mon':
        col = 'D'
    elif day == 'Tue':
        col = 'E'
    elif day == 'Wed':
        col = 'F'
    elif day == 'Thu':
        col = 'G'
    elif day == 'Fri':
        col = 'H'
    elif day == 'Sat':
        col = 'I'
    elif day == 'Sun':
        col = 'J'

    return col


def openbrowser(url, col, row):
    url = url + str(col) + str(row)
    print(url)
    webbrowser.open(url)


def get_time():
    now = datetime.datetime.now()
    return str(now.strftime('%H:%M'))


def typing():
    pg.hotkey('ctrl', 'c')
    text = str(pyperclip.paste())
    pyperclip.copy('')  #emptyed in clipbord
    if len(text) > 2:  #exit words in cell
        text = text.replace('.', '')  # replace dot to empty なぜかドットが入る
        t_index = text.find('-')  #find text index
        text = text[:t_index + 1]
        text = text + str(get_time()) + " 勉強のため"
        pg.hotkey('delete')
    elif len(text) <= 2:  #empty cell なぜか空白には長さが2ある
        text = get_time() + " - "
    print(text)
    success_code = "SUCCESS"
    print(success_code)

    pyperclip.copy(text)
    pg.hotkey('Enter')
    pg.hotkey('ctrl', 'v')
    pg.hotkey('Enter')


def wait(max_wait_time):
    time.sleep(3)
    count = 0  #待ちカウント保持
    # pg.doubleClick(10, 10)
    for i in range(max_wait_time):
        try:
            x = pg.locateCenterOnScreen("./image/drive.png")
            if x != "none":
                print("ready to write:", x)
                break
        except Exception as ex:
            x = "none"
            count += 1
            if count > max_wait_time:
                sys.exit(-1)
            print("wait...")


def close_chrome():
    time.sleep(5)  #修正したい
    os.system("taskkill /im chrome.exe /f")  #exit chrome


def main():
    max_wait_time = 20  #最大待ち時間
    row, url, ssid = file_read()

    try:
        if get_ssid() in ssid:
            openbrowser(url, get_col(), row)
            wait(max_wait_time)
            typing()
            # close_chrome()  #chromeを閉じたいとき

    except Exception as ex:
        print(ex)
        print('wifiに接続していない可能性があります')
        sys.exit(-1)


if __name__ == '__main__':
    main()
    sys.exit(0)
