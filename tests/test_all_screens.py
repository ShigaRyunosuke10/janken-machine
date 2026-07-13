#!/usr/bin/env python3
"""
すべての画面表示をテスト
各画面を2秒ずつ表示して動作確認
"""

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from matrix_display import MatrixDisplay

def main():
    print("=" * 50)
    print("Testing all display screens")
    print("=" * 50)

    display = MatrixDisplay()

    try:
        # 1. PUSH START画面
        print("\n1. Testing show_push_start()...")
        display.show_push_start()
        time.sleep(2)

        # 2. カウントダウン（単独）
        print("2. Testing show_countdown()...")
        for count in [3, 2, 1]:
            print(f"   Count: {count}")
            display.show_countdown(count)
            time.sleep(1)

        # 3. SELECT + カウントダウン（新）
        print("3. Testing show_choice_prompt_with_countdown()...")
        for count in [3, 2, 1]:
            print(f"   SELECT + Count: {count}")
            display.show_choice_prompt_with_countdown(count)
            time.sleep(1)

        # 4. SELECT YOUR HAND画面（カウントダウンなし）
        print("4. Testing show_choice_prompt()...")
        display.show_choice_prompt()
        time.sleep(2)

        # 5. プレイヤーの手表示
        print("5. Testing show_hand() for player...")
        for hand in ['rock', 'scissors', 'paper']:
            print(f"   Player hand: {hand}")
            display.show_hand(hand, is_player=True)
            time.sleep(1.5)

        # 6. VS画面
        print("6. Testing show_vs_screen()...")
        display.show_vs_screen('rock', 'scissors')
        time.sleep(2)

        # 7. 結果画面
        print("7. Testing show_result()...")
        for result in ['win', 'lose', 'draw']:
            print(f"   Result: {result}")
            display.show_result(result)
            time.sleep(2)

        # 8. 塗りつぶし
        print("8. Testing fill_color()...")
        colors = [
            (255, 0, 0, "Red"),
            (0, 255, 0, "Green"),
            (0, 0, 255, "Blue")
        ]
        for r, g, b, name in colors:
            print(f"   Fill: {name}")
            display.fill_color(r, g, b)
            time.sleep(1)

        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        print("=" * 50)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        display.cleanup()
        print("Cleanup done")

if __name__ == '__main__':
    main()
