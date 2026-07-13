#!/usr/bin/env python3
"""
ボタンLED出力テストプログラム
GPIO 2, 3, 14, 15 のLED出力を確認
"""

from gpiozero import LED
import time

# GPIO ピン定義
PIN_START_LED = 2
PIN_RED_LED = 3
PIN_YELLOW_LED = 14
PIN_BLUE_LED = 15

# LED初期化
led_start = LED(PIN_START_LED)
led_red = LED(PIN_RED_LED)
led_yellow = LED(PIN_YELLOW_LED)
led_blue = LED(PIN_BLUE_LED)

def test_all_on():
    """全LEDを点灯"""
    print("Test 1: All LEDs ON")
    led_start.on()
    led_red.on()
    led_yellow.on()
    led_blue.on()
    time.sleep(2)

def test_all_off():
    """全LEDを消灯"""
    print("Test 2: All LEDs OFF")
    led_start.off()
    led_red.off()
    led_yellow.off()
    led_blue.off()
    time.sleep(1)

def test_individual():
    """個別点灯テスト"""
    print("Test 3: Individual LED test")

    leds = [
        (led_start, "START (White)"),
        (led_red, "RED (Rock)"),
        (led_yellow, "YELLOW (Scissors)"),
        (led_blue, "BLUE (Paper)")
    ]

    for led, name in leds:
        print(f"  - {name}: ON")
        led.on()
        time.sleep(0.8)
        led.off()
        time.sleep(0.2)

def test_blink():
    """点滅テスト"""
    print("Test 4: Blink test (3 times)")

    for i in range(3):
        print(f"  - Blink {i+1}/3")
        led_start.on()
        led_red.on()
        led_yellow.on()
        led_blue.on()
        time.sleep(0.3)

        led_start.off()
        led_red.off()
        led_yellow.off()
        led_blue.off()
        time.sleep(0.3)

def test_wave():
    """ウェーブパターンテスト"""
    print("Test 5: Wave pattern")

    leds = [led_start, led_red, led_yellow, led_blue]

    for _ in range(2):
        for led in leds:
            led.on()
            time.sleep(0.2)
            led.off()

def cleanup():
    """終了処理：全LED消灯"""
    print("\nCleanup: Turning off all LEDs")
    led_start.off()
    led_red.off()
    led_yellow.off()
    led_blue.off()

if __name__ == "__main__":
    print("=" * 50)
    print("Button LED Output Test")
    print("=" * 50)
    print("Testing GPIO 2, 3, 14, 15")
    print("=" * 50)
    print()

    try:
        test_all_on()
        test_all_off()
        test_individual()
        test_blink()
        test_wave()

        print()
        print("=" * 50)
        print("All tests completed successfully!")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
    finally:
        cleanup()
