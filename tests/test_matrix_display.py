#!/usr/bin/env python3
"""
LEDマトリックス表示テストプログラム
64x64 RGB LEDマトリックス（32x64 × 2枚）での表示確認
"""

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

# マトリックス設定（src/matrix_display.py と同じ動作確認済み設定）
options = RGBMatrixOptions()
options.rows = 32                          # 1パネルの行数
options.cols = 64                          # 1パネルの列数
options.chain_length = 1
options.parallel = 2                       # 2枚を並列接続（縦方向64x64）
options.hardware_mapping = 'regular'
options.disable_hardware_pulsing = True    # ソフトウェアパルス（重要）
options.gpio_slowdown = 5                  # タイミング調整（重要）

# マトリックス初期化
matrix = RGBMatrix(options=options)

# フォント読み込み
font = graphics.Font()
font.LoadFont("/home/janken/rpi-rgb-led-matrix/fonts/7x13.bdf")

# 色定義
COLOR_RED = graphics.Color(255, 0, 0)
COLOR_GREEN = graphics.Color(0, 255, 0)
COLOR_BLUE = graphics.Color(0, 0, 255)
COLOR_YELLOW = graphics.Color(255, 255, 0)
COLOR_WHITE = graphics.Color(255, 255, 255)
COLOR_CYAN = graphics.Color(0, 255, 255)
COLOR_MAGENTA = graphics.Color(255, 0, 255)

def clear_screen():
    """画面クリア"""
    matrix.Clear()

def test_solid_colors():
    """単色塗りつぶしテスト"""
    print("Test 1: Solid colors")

    colors = [
        (COLOR_RED, "Red"),
        (COLOR_GREEN, "Green"),
        (COLOR_BLUE, "Blue"),
        (COLOR_YELLOW, "Yellow"),
        (COLOR_WHITE, "White")
    ]

    for color, name in colors:
        print(f"  - {name}")
        canvas = matrix.CreateFrameCanvas()
        for x in range(64):
            for y in range(64):
                canvas.SetPixel(x, y, color.red, color.green, color.blue)
        matrix.SwapOnVSync(canvas)
        time.sleep(1)

def test_text_display():
    """テキスト表示テスト"""
    print("Test 2: Text display")

    texts = [
        ("PUSH", COLOR_GREEN, 20),
        ("START", COLOR_CYAN, 35),
        ("ROCK", COLOR_RED, 20),
        ("PAPER", COLOR_BLUE, 35),
        ("WIN!", COLOR_YELLOW, 20)
    ]

    for text, color, y_pos in texts:
        print(f"  - '{text}'")
        canvas = matrix.CreateFrameCanvas()
        canvas.Clear()

        # テキストを中央寄せで表示
        text_width = len(text) * 7  # 7x13フォントの幅は約7px
        x_pos = (64 - text_width) // 2

        graphics.DrawText(canvas, font, x_pos, y_pos, color, text)
        matrix.SwapOnVSync(canvas)
        time.sleep(1.5)

def test_countdown():
    """カウントダウン表示テスト"""
    print("Test 3: Countdown (3, 2, 1)")

    for count in [3, 2, 1]:
        canvas = matrix.CreateFrameCanvas()
        canvas.Clear()

        # 数字を大きく表示（中央）
        graphics.DrawText(canvas, font, 28, 35, COLOR_YELLOW, str(count))
        matrix.SwapOnVSync(canvas)
        time.sleep(0.8)

def test_multiline_text():
    """複数行テキスト表示テスト"""
    print("Test 4: Multi-line text")

    canvas = matrix.CreateFrameCanvas()
    canvas.Clear()

    lines = [
        ("PUSH", COLOR_GREEN, 15),
        ("START", COLOR_CYAN, 30),
        ("BUTTON", COLOR_WHITE, 45)
    ]

    for text, color, y_pos in lines:
        text_width = len(text) * 7
        x_pos = (64 - text_width) // 2
        graphics.DrawText(canvas, font, x_pos, y_pos, color, text)

    matrix.SwapOnVSync(canvas)
    time.sleep(3)

def test_animation():
    """簡単なアニメーションテスト"""
    print("Test 5: Simple animation")

    for i in range(20):
        canvas = matrix.CreateFrameCanvas()
        canvas.Clear()

        # 円を描く
        center_x, center_y = 32, 32
        radius = 10 + i
        color_val = (i * 12) % 255

        for angle in range(0, 360, 10):
            import math
            rad = math.radians(angle)
            x = int(center_x + radius * math.cos(rad))
            y = int(center_y + radius * math.sin(rad))

            if 0 <= x < 64 and 0 <= y < 64:
                canvas.SetPixel(x, y, color_val, 255 - color_val, 128)

        matrix.SwapOnVSync(canvas)
        time.sleep(0.05)

def cleanup():
    """終了処理：画面クリア"""
    print("\nCleanup: Clearing display")
    clear_screen()

if __name__ == "__main__":
    print("=" * 50)
    print("LED Matrix Display Test")
    print("=" * 50)
    print("Resolution: 64x64 (32x64 x 2 panels)")
    print("=" * 50)
    print()

    try:
        test_solid_colors()
        clear_screen()
        time.sleep(0.5)

        test_text_display()
        clear_screen()
        time.sleep(0.5)

        test_countdown()
        clear_screen()
        time.sleep(0.5)

        test_multiline_text()
        clear_screen()
        time.sleep(0.5)

        test_animation()
        clear_screen()

        print()
        print("=" * 50)
        print("All tests completed successfully!")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup()
