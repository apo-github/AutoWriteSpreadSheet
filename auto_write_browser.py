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
    return row, url


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


def main():
    try:
        if get_ssid() == "HINES-WLAN":
            row, url = file_read()
            openbrowser(url, get_col(), row)
            wait()
            typing()

            # time.sleep(5)
            # os.system("taskkill /im chrome.exe /f")  #exit chrome
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()

#セルに既に文字列があった場合
#まず文字列を取得し，ハイフンの後ろのみを変更
# 8:30 - 19:00 勉強のため

#セルに文字列がなかった場合
#時間＋ハイフンを代入
#8:30 - など

#send to cell a timestamp
# sheet.update_cell(
#     12, 8,
#     "8:50-19:30 ミーティングのため")  #(row, col(H) , "words that you send to cell")