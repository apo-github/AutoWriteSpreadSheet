import webbrowser
import datetime
import subprocess
from subprocess import PIPE
import pyautogui as pg
import pyperclip
import time
import os


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
        t_index = text.find('-')  #find text index
        text = text[:t_index + 1]
        text = text + str(get_time()) + " 勉強のため"
        pg.hotkey('delete')
    elif len(text) <= 2:  #empty cell なぜか空白には長さが2ある
        text = get_time() + "-"
    print(text)

    pyperclip.copy(text)
    pg.hotkey('Enter')
    pg.hotkey('ctrl', 'v')
    pg.hotkey('Enter')


def wait():
    time.sleep(3)
    # pg.doubleClick(10, 10)
    for i in range(100):
        try:
            x = pg.locateCenterOnScreen("./image/meeting.png")
            if x != "none":
                print("ready to write:", x)
                break
        except Exception as ex:
            x = "none"
            print("wait...")


def close_chrome():
    time.sleep(5)  #修正したい
    os.system("taskkill /im chrome.exe /f")  #exit chrome


def main():
    row, url, ssid = file_read()

    try:
        if get_ssid() in ssid:
            openbrowser(url, get_col(), row)
            wait()
            typing()
            close_chrome()  #chromeを閉じたいとき

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
