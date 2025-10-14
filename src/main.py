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
        self.win_streak = 0  # 連勝カウンター

    def wait_for_start(self):
        """スタート待機状態（隠しコマンド対応）"""
        print("=== Waiting for START button ===")

        # ディスプレイ: PUSH START
        self.display.show_push_start()

        # スタートボタンLEDを点滅
        self.buttons.start_blink('start', interval=0.5)

        # 他のLEDは消灯
        self.buttons.set_led('red', False)
        self.buttons.set_led('yellow', False)
        self.buttons.set_led('blue', False)

        # 隠しコマンドシーケンス: 赤→黄→青→青→黄→赤
        secret_sequence = ['red', 'yellow', 'blue', 'blue', 'yellow', 'red']
        input_sequence = []
        last_button_time = time.time()

        # スタートボタンが押されるまで待機（隠しコマンドチェック付き）
        while True:
            # タイムアウト: 5秒間入力がなければシーケンスリセット
            if time.time() - last_button_time > 5.0:
                if len(input_sequence) > 0:
                    print("  Secret sequence timeout - reset")
                    input_sequence = []

            # スタートボタンチェック
            if self.buttons.is_button_pressed('start'):
                break

            # 隠しコマンドボタンチェック
            for button in ['red', 'yellow', 'blue']:
                if self.buttons.is_button_pressed(button):
                    input_sequence.append(button)
                    last_button_time = time.time()
                    print(f"  Secret input: {button} (sequence: {len(input_sequence)}/6)")

                    # シーケンス確認
                    if input_sequence == secret_sequence:
                        print("  SECRET COMMAND ACTIVATED!")
                        self.show_secret_easter_egg()
                        input_sequence = []
                        # スタート画面に戻る
                        self.display.show_push_start()
                    elif len(input_sequence) >= len(secret_sequence):
                        # シーケンスが長すぎる場合はリセット
                        print("  Wrong sequence - reset")
                        input_sequence = []
                    elif input_sequence != secret_sequence[:len(input_sequence)]:
                        # 途中で間違った場合もリセット
                        print("  Wrong button - reset")
                        input_sequence = []

                    time.sleep(0.3)  # チャタリング防止
                    break

            time.sleep(0.05)

        # スタートボタンLED点灯に切り替え
        self.buttons.stop_blink('start')
        self.buttons.set_led('start', True)

        print("START button pressed!")

        # スタートボタンLED消灯
        self.buttons.set_led('start', False)

    def show_secret_easter_egg(self):
        """隠しメッセージ演出"""
        print("=== EASTER EGG ===")

        # スタートボタン点滅停止
        self.buttons.stop_blink('start')

        # 全LEDレインボー演出
        colors = [
            ('red', True, False, False),
            ('yellow', False, True, False),
            ('blue', False, False, True),
            ('all', True, True, True)
        ]

        for _ in range(3):
            for name, r, y, b in colors:
                self.buttons.set_led('red', r)
                self.buttons.set_led('yellow', y)
                self.buttons.set_led('blue', b)
                time.sleep(0.15)

        # 隠しメッセージ表示
        self.display.show_secret_message()

        # 全LED点灯
        self.buttons.set_led('red', True)
        self.buttons.set_led('yellow', True)
        self.buttons.set_led('blue', True)
        self.buttons.set_led('start', True)

        time.sleep(3)

        # LED消灯
        self.buttons.all_leds_off()

        # スタートボタン点滅再開
        self.buttons.start_blink('start', interval=0.5)

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

        # 選択ボタンLEDを全点滅開始
        self.buttons.start_all_blink(interval=0.3)

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
                        # チェイス点滅を停止して選択ボタンのみ点灯
                        self.buttons.stop_all_blinks()
                        time.sleep(0.1)  # 停止処理が完了するまで待機
                        self.buttons.set_led('red', True)
                        self.buttons.set_led('yellow', False)
                        self.buttons.set_led('blue', False)
                        break  # すぐにループを抜ける
                    elif self.buttons.is_button_pressed('yellow'):
                        selected_hand = 'scissors'
                        print(f"  Player selected: {selected_hand}")
                        self.buttons.stop_all_blinks()
                        time.sleep(0.1)
                        self.buttons.set_led('red', False)
                        self.buttons.set_led('yellow', True)
                        self.buttons.set_led('blue', False)
                        break  # すぐにループを抜ける
                    elif self.buttons.is_button_pressed('blue'):
                        selected_hand = 'paper'
                        print(f"  Player selected: {selected_hand}")
                        self.buttons.stop_all_blinks()
                        time.sleep(0.1)
                        self.buttons.set_led('red', False)
                        self.buttons.set_led('yellow', False)
                        self.buttons.set_led('blue', True)
                        break  # すぐにループを抜ける

                time.sleep(0.05)

            # 選択されたらforループも抜ける
            if selected_hand is not None:
                break

        # 5秒経過後、選択されていない場合は時間切れ
        if selected_hand is None:
            print(f"  No selection - Timeout!")
            self.buttons.stop_all_blinks()

            # 念のため全ボタンLEDを明示的に消灯
            self.buttons.set_led('red', False)
            self.buttons.set_led('yellow', False)
            self.buttons.set_led('blue', False)

            # 時間切れメッセージを表示
            self.display.show_no_selection()
            time.sleep(2)

            # Noneを返して最初に戻る
            return None

        # 選択されたのでそのまま返す（5秒待たない）
        return selected_hand

    def ask_continue(self):
        """
        続行確認（5秒間スタートボタン待機）

        Returns:
            True=続行, False=終了
        """
        print("=== Ask Continue ===")

        # スタートボタンLEDを点滅
        self.buttons.start_blink('start', interval=0.3)

        # 5秒間カウントダウンしながらスタートボタンを待つ
        for countdown in [5, 4, 3, 2, 1]:
            # カウントダウン付き続行確認画面を表示
            self.display.show_continue_prompt(self.win_streak, countdown)

            count_start = time.time()

            # 1秒間ボタン入力をチェック
            while time.time() - count_start < 1.0:
                if self.buttons.is_button_pressed('start'):
                    print("  Continue!")
                    self.buttons.stop_blink('start')
                    self.buttons.set_led('start', False)
                    return True
                time.sleep(0.05)

        # タイムアウト
        print("  Timeout - Reset")
        self.buttons.stop_blink('start')
        self.buttons.set_led('start', False)
        return False

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
        time.sleep(1.5)

        # 結果表示（連勝数付き）
        self.display.show_result(result, self.win_streak)

        # LED演出
        if result == 'win':
            # 勝利: 全LED点滅
            for _ in range(4):
                self.buttons.all_leds_on()
                time.sleep(0.15)
                self.buttons.all_leds_off()
                time.sleep(0.15)
        elif result == 'lose':
            # 敗北: スタートボタンのみ点滅
            for _ in range(3):
                self.buttons.set_led('start', True)
                time.sleep(0.25)
                self.buttons.set_led('start', False)
                time.sleep(0.25)
        else:
            # 引き分け: 選択ボタン同時点滅
            for _ in range(3):
                self.buttons.set_led('red', True)
                self.buttons.set_led('yellow', True)
                self.buttons.set_led('blue', True)
                time.sleep(0.25)
                self.buttons.set_led('red', False)
                self.buttons.set_led('yellow', False)
                self.buttons.set_led('blue', False)
                time.sleep(0.25)

        time.sleep(1)

    def run_game_loop(self):
        """ゲームループ（連勝システム対応）"""
        try:
            while True:
                # 1. スタート待機
                self.wait_for_start()

                # ゲームセッション開始
                while True:
                    # 2. カウントダウン + 手選択（統合・5秒）
                    player_hand = self.countdown_and_selection()

                    # 時間切れの場合はリセット
                    if player_hand is None:
                        print("=== Timeout - Reset ===\n")
                        self.win_streak = 0
                        time.sleep(1)
                        break  # スタート画面に戻る

                    # 3. CPU手選択
                    cpu_hand = self.cpu_selection()

                    # 4. 勝敗判定
                    result = self.judge(player_hand, cpu_hand)

                    # 5. 結果表示
                    if result == 'win':
                        # 勝った場合：連勝数を増やす
                        self.win_streak += 1
                        print(f"Win! Streak: {self.win_streak}")

                    self.show_result(player_hand, cpu_hand, result)

                    # 6. 続行判定
                    if result == 'lose':
                        # 負けた場合：リセットしてスタート画面へ
                        print("=== Lose - Reset ===\n")
                        self.win_streak = 0
                        # LED演出とshow_result最後の待機時間を含めて既に時間が経過しているのでそのまま遷移
                        break
                    elif result == 'win':
                        # 勝った場合：続行確認
                        if self.ask_continue():
                            # 続行
                            continue
                        else:
                            # タイムアウト：リセット
                            print("=== Timeout - Reset ===\n")
                            self.win_streak = 0
                            break
                    elif result == 'draw':
                        # あいこの場合
                        if self.win_streak > 0:
                            # 連勝中：続行確認
                            if self.ask_continue():
                                # 続行
                                continue
                            else:
                                # タイムアウト：リセット
                                print("=== Timeout - Reset ===\n")
                                self.win_streak = 0
                                break
                        else:
                            # 連勝していない：直接スタート画面へ
                            print("=== Draw - Return to Start ===\n")
                            # LED演出とshow_result最後の待機時間を含めて既に時間が経過しているのでそのまま遷移
                            break

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
