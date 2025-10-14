#!/usr/bin/env python3
"""
じゃんけんマシン メインプログラム
Raspberry Pi 4B + LED Matrix + Buttons
"""

import random
import time
from button_controller import ButtonController
from matrix_display import MatrixDisplay

class JankenGame:
    """じゃんけんゲームのメインロジック"""

    def __init__(self):
        self.buttons = ButtonController()
        self.display = MatrixDisplay()
        self.hands = ['rock', 'scissors', 'paper']

    def wait_for_start(self):
        """スタート待機状態"""
        print("=== Waiting for START button ===")

        # ディスプレイ: PUSH START
        self.display.show_push_start()

        # スタートボタンLEDを点滅
        self.buttons.start_blink('start', interval=0.5)

        # 他のLEDは消灯
        self.buttons.set_led('red', False)
        self.buttons.set_led('yellow', False)
        self.buttons.set_led('blue', False)

        # スタートボタンが押されるまで待機
        self.buttons.wait_for_button('start')

        # スタートボタンLED点灯に切り替え
        self.buttons.stop_blink('start')
        self.buttons.set_led('start', True)

        print("START button pressed!")
        time.sleep(0.3)

    def countdown_and_selection(self):
        """
        カウントダウン + 手選択（統合）
        5秒間のカウントダウン中にボタン選択可能

        Returns:
            'rock', 'scissors', 'paper' or None (timeout)
        """
        print("=== Countdown + Selection ===")

        # スタートボタンLED点灯
        self.buttons.set_led('start', True)

        # 選択ボタンLEDを点滅開始
        self.buttons.start_blink('red', interval=0.3)
        self.buttons.start_blink('yellow', interval=0.3)
        self.buttons.start_blink('blue', interval=0.3)

        selected_hand = None
        start_time = time.time()

        # 5秒間のカウントダウン + 選択受付
        for count in [5, 4, 3, 2, 1]:
            print(f"  {count}...")
            self.display.show_choice_prompt_with_countdown(count)

            count_start = time.time()

            # 1秒間ボタン入力をチェック
            while time.time() - count_start < 1.0:
                if selected_hand is None:
                    if self.buttons.is_button_pressed('red'):
                        selected_hand = 'rock'
                        print(f"  Player selected: {selected_hand}")
                        # 選択されたボタンのみ点灯（他は消灯）
                        self.buttons.stop_all_blinks()
                        self.buttons.set_led('red', True)
                        self.buttons.set_led('yellow', False)
                        self.buttons.set_led('blue', False)
                    elif self.buttons.is_button_pressed('yellow'):
                        selected_hand = 'scissors'
                        print(f"  Player selected: {selected_hand}")
                        self.buttons.stop_all_blinks()
                        self.buttons.set_led('red', False)
                        self.buttons.set_led('yellow', True)
                        self.buttons.set_led('blue', False)
                    elif self.buttons.is_button_pressed('blue'):
                        selected_hand = 'paper'
                        print(f"  Player selected: {selected_hand}")
                        self.buttons.stop_all_blinks()
                        self.buttons.set_led('red', False)
                        self.buttons.set_led('yellow', False)
                        self.buttons.set_led('blue', True)

                time.sleep(0.05)

        # 5秒経過後、選択されていない場合は時間切れ
        if selected_hand is None:
            print(f"  No selection - Timeout!")
            self.buttons.stop_all_blinks()

            # 時間切れメッセージを表示
            self.display.show_no_selection()
            time.sleep(2)

            # Noneを返して最初に戻る
            return None

        # 残り時間を待機（5秒経過まで）
        elapsed = time.time() - start_time
        if elapsed < 5.0:
            wait_time = 5.0 - elapsed
            print(f"  Waiting {wait_time:.1f}s before result...")
            time.sleep(wait_time)

        return selected_hand

    def cpu_selection(self):
        """
        CPUの手選択（ランダム）

        Returns:
            'rock', 'scissors', 'paper'
        """
        cpu_hand = random.choice(self.hands)
        print(f"  CPU selected: {cpu_hand}")
        return cpu_hand

    def judge(self, player_hand: str, cpu_hand: str):
        """
        勝敗判定

        Args:
            player_hand: プレイヤーの手
            cpu_hand: CPUの手

        Returns:
            'win', 'lose', 'draw'
        """
        if player_hand == cpu_hand:
            return 'draw'

        win_conditions = {
            'rock': 'scissors',
            'scissors': 'paper',
            'paper': 'rock'
        }

        if win_conditions[player_hand] == cpu_hand:
            return 'win'
        else:
            return 'lose'

    def show_result(self, player_hand: str, cpu_hand: str, result: str):
        """結果表示"""
        print(f"=== Result: {result.upper()} ===")

        # 対決画面表示
        self.display.show_vs_screen(player_hand, cpu_hand)
        time.sleep(2)

        # 結果表示
        self.display.show_result(result)

        # LED演出
        if result == 'win':
            # 勝利: 全LED点滅
            for _ in range(5):
                self.buttons.all_leds_on()
                time.sleep(0.2)
                self.buttons.all_leds_off()
                time.sleep(0.2)
        elif result == 'lose':
            # 敗北: スタートボタンのみ点滅
            for _ in range(3):
                self.buttons.set_led('start', True)
                time.sleep(0.3)
                self.buttons.set_led('start', False)
                time.sleep(0.3)
        else:
            # 引き分け: 選択ボタン同時点滅
            for _ in range(3):
                self.buttons.set_led('red', True)
                self.buttons.set_led('yellow', True)
                self.buttons.set_led('blue', True)
                time.sleep(0.3)
                self.buttons.set_led('red', False)
                self.buttons.set_led('yellow', False)
                self.buttons.set_led('blue', False)
                time.sleep(0.3)

        time.sleep(2)

    def run_game_loop(self):
        """ゲームループ"""
        try:
            while True:
                # 1. スタート待機
                self.wait_for_start()

                # 2. カウントダウン + 手選択（統合・5秒）
                player_hand = self.countdown_and_selection()

                # 時間切れの場合は最初に戻る
                if player_hand is None:
                    print("=== Timeout - Return to start ===\n")
                    time.sleep(1)
                    continue

                # 3. CPU手選択
                cpu_hand = self.cpu_selection()

                # 4. 勝敗判定
                result = self.judge(player_hand, cpu_hand)

                # 5. 結果表示
                self.show_result(player_hand, cpu_hand, result)

                # 6. 次のゲームへ（自動リセット）
                print("=== Auto reset in 3 seconds ===\n")
                time.sleep(3)

        except KeyboardInterrupt:
            print("\n\nGame terminated by user")
        except Exception as e:
            print(f"\n\nError occurred: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()

    def cleanup(self):
        """終了処理"""
        print("Cleanup...")
        self.buttons.cleanup()
        self.display.cleanup()
        print("Done.")

if __name__ == "__main__":
    print("=" * 50)
    print("Rock-Paper-Scissors Machine")
    print("=" * 50)
    print()

    game = JankenGame()
    game.run_game_loop()
