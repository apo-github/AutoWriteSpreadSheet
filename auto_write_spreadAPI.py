import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import subprocess
from subprocess import PIPE

users = {"村山風輝": 12}  #{"key" : value} / dictionary_name["key"] = value


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
            print('ssid = ' + ssid)
        elif data.find('    BSSID') == 0:
            bssid = data[data.find(':') + 2:len(data)]
            print('bssid = ' + bssid)

    return ssid

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

# use creds to create a client to interact with the Google Drive API
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'autowritespreadsheet-348009-e87f7e5ee490.json', scope)
client = gspread.authorize(creds)

#sheet title
sheet = client.open("syukkinsheet").sheet1

#create a word #全てのセルを取得し，月日の文字列の一致から代入したい行列を特定
dt_now = datetime.date.today()
m_d = "{0}月{1}日".format(dt_now.month, dt_now.day)  #今の日付を取得

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