#!/usr/bin/env python3
"""
ボタン入力テストプログラム
GPIO 0, 1, 16, 26 のボタン入力を確認
"""

from gpiozero import Button
from signal import pause
import time

# GPIO ピン定義
PIN_START = 0
PIN_RED = 1
PIN_YELLOW = 16
PIN_BLUE = 26

# ボタン初期化
button_start = Button(PIN_START, pull_up=True)
button_red = Button(PIN_RED, pull_up=True)
button_yellow = Button(PIN_YELLOW, pull_up=True)
button_blue = Button(PIN_BLUE, pull_up=True)

def on_start_pressed():
    """スタートボタンが押された時"""
    print(f"[{time.strftime('%H:%M:%S')}] ★ START button pressed!")

def on_red_pressed():
    """赤ボタン（グー）が押された時"""
    print(f"[{time.strftime('%H:%M:%S')}] 🔴 RED button pressed (Rock)")

def on_yellow_pressed():
    """黄ボタン（チョキ）が押された時"""
    print(f"[{time.strftime('%H:%M:%S')}] 🟡 YELLOW button pressed (Scissors)")

def on_blue_pressed():
    """青ボタン（パー）が押された時"""
    print(f"[{time.strftime('%H:%M:%S')}] 🔵 BLUE button pressed (Paper)")

# イベントハンドラ登録
button_start.when_pressed = on_start_pressed
button_red.when_pressed = on_red_pressed
button_yellow.when_pressed = on_yellow_pressed
button_blue.when_pressed = on_blue_pressed

if __name__ == "__main__":
    print("=" * 50)
    print("Button Input Test")
    print("=" * 50)
    print("Press any button to test...")
    print("- START: White button")
    print("- RED: Rock (グー)")
    print("- YELLOW: Scissors (チョキ)")
    print("- BLUE: Paper (パー)")
    print("Press Ctrl+C to exit")
    print("=" * 50)

    try:
        pause()
    except KeyboardInterrupt:
        print("\nTest terminated.")
