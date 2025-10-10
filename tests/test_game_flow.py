#!/usr/bin/env python3
"""
ゲームフロー全体のテスト（ボタン入力なし）
各ステップを自動的に進めて動作確認
"""

import sys
import time
import random
sys.path.insert(0, '/home/janken/janken-machine/src')

from matrix_display import MatrixDisplay

def test_game_flow():
    """ゲームフローのテスト"""
    display = MatrixDisplay()

    try:
        print("=" * 50)
        print("Game Flow Test (Auto Mode)")
        print("=" * 50)

        # 1. 待機画面
        print("\n[1] Waiting for START...")
        display.show_push_start()
        time.sleep(2)
        print("    (Simulating START button press)")
        time.sleep(0.5)

        # 2. カウントダウン + SELECT表示
        print("\n[2] Countdown + SELECT...")
        for count in [3, 2, 1]:
            print(f"    {count}...")
            display.show_choice_prompt_with_countdown(count)
            time.sleep(0.8)

        # 3. 手選択画面
        print("\n[3] Waiting for player selection...")
        display.show_choice_prompt()
        time.sleep(1.5)

        # 4. プレイヤー選択（ランダム）
        hands = ['rock', 'scissors', 'paper']
        player_hand = random.choice(hands)
        print(f"    Player selected: {player_hand}")
        display.show_hand(player_hand, is_player=True)
        time.sleep(1.5)

        # 5. CPU選択（ランダム）
        cpu_hand = random.choice(hands)
        print(f"    CPU selected: {cpu_hand}")

        # 6. 勝敗判定
        def judge(p_hand, c_hand):
            if p_hand == c_hand:
                return 'draw'
            win_conditions = {
                'rock': 'scissors',
                'scissors': 'paper',
                'paper': 'rock'
            }
            if win_conditions[p_hand] == c_hand:
                return 'win'
            else:
                return 'lose'

        result = judge(player_hand, cpu_hand)
        print(f"    Result: {result.upper()}")

        # 7. VS画面
        print("\n[4] Showing VS screen...")
        display.show_vs_screen(player_hand, cpu_hand)
        time.sleep(2)

        # 8. 結果表示
        print(f"\n[5] Showing result: {result.upper()}")
        display.show_result(result)
        time.sleep(2)

        print("\n" + "=" * 50)
        print("Game flow test completed!")
        print("=" * 50)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        display.cleanup()
        print("Cleanup done")

if __name__ == '__main__':
    # 3回ゲームを回す
    for i in range(3):
        print(f"\n{'=' * 50}")
        print(f"GAME {i + 1}/3")
        print('=' * 50)
        test_game_flow()
        if i < 2:
            print("\nNext game in 3 seconds...")
            time.sleep(3)
