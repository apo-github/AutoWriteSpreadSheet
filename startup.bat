@rem /s シャットダウン /f アプリケーションを強制終了する /t 何秒後に起動するか
@rem start /wait の後，コマンドを指定することで処理が終わってから次のコマンドが実行される
@rem python スクリプトパス で実行できる
@rem C:\Users\ユーザー名\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startupにbatを入れておけば起動時に実行される
@rem echo off コマンドを繰り返さない
@rem chcp unicodeをutf8で開く

@echo off
chcp 65001
timeout 10 >nul
cd C:\Users\fukic\Documents\Syoriken\python\auto\出所記録表
python auto_write_browser.py
if %errorlevel% neq 0(
    echo wifiにつながっていません.
    pause
)
exit