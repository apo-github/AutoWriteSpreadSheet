@rem timeout timeout x : x秒後に実行
@rem >nul : timeoutカウントダウンを非表示

@echo off
chcp 65001
cd C:\Users\スクリプトパス
timeout 1 >nul

start /wait python auto_write_browser.py
if %errorlevel% neq 0(
    echo wifiにつながっていません.
    exit /b
)
start /wait shutdown /s /f /t 0 
