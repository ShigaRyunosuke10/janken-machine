"""
ボタンコントローラーモジュール
ボタン入力とLED出力を管理
"""

from gpiozero import Button, LED
import threading
import time

# GPIO ピン定義
PIN_START = 0
PIN_RED = 1
PIN_YELLOW = 16
PIN_BLUE = 26

PIN_START_LED = 2
PIN_RED_LED = 3
PIN_YELLOW_LED = 14
PIN_BLUE_LED = 15

class ButtonController:
    """ボタン入力・LED出力を統合管理するクラス"""

    def __init__(self):
        # ボタン初期化
        self.button_start = Button(PIN_START, pull_up=True)
        self.button_red = Button(PIN_RED, pull_up=True)
        self.button_yellow = Button(PIN_YELLOW, pull_up=True)
        self.button_blue = Button(PIN_BLUE, pull_up=True)

        # LED初期化（active_low=True で点灯・消灯を反転）
        self.led_start = LED(PIN_START_LED, active_high=False)
        self.led_red = LED(PIN_RED_LED, active_high=False)
        self.led_yellow = LED(PIN_YELLOW_LED, active_high=False)
        self.led_blue = LED(PIN_BLUE_LED, active_high=False)

        # 点滅制御用
        self._blink_threads = {}
        self._blink_stop_flags = {}

    def set_led(self, led_name: str, state: bool):
        """
        指定したLEDの状態を変更

        Args:
            led_name: 'start', 'red', 'yellow', 'blue'
            state: True=点灯, False=消灯
        """
        led_map = {
            'start': self.led_start,
            'red': self.led_red,
            'yellow': self.led_yellow,
            'blue': self.led_blue
        }

        if led_name in led_map:
            if state:
                led_map[led_name].on()
            else:
                led_map[led_name].off()

    def start_blink(self, led_name: str, interval: float = 0.5):
        """
        指定したLEDを点滅開始

        Args:
            led_name: 'start', 'red', 'yellow', 'blue'
            interval: 点滅間隔（秒）
        """
        # 既存の点滅を停止
        self.stop_blink(led_name)

        # 停止フラグを作成
        stop_flag = threading.Event()
        self._blink_stop_flags[led_name] = stop_flag

        # 点滅スレッド開始
        thread = threading.Thread(
            target=self._blink_worker,
            args=(led_name, interval, stop_flag),
            daemon=True
        )
        self._blink_threads[led_name] = thread
        thread.start()

    def _blink_worker(self, led_name: str, interval: float, stop_flag: threading.Event):
        """点滅処理のワーカー"""
        state = True
        while not stop_flag.is_set():
            self.set_led(led_name, state)
            state = not state
            time.sleep(interval)

        # スレッド終了時に必ず消灯
        self.set_led(led_name, False)

    def stop_blink(self, led_name: str):
        """
        指定したLEDの点滅を停止

        Args:
            led_name: 'start', 'red', 'yellow', 'blue'
        """
        if led_name in self._blink_stop_flags:
            self._blink_stop_flags[led_name].set()

            if led_name in self._blink_threads:
                self._blink_threads[led_name].join(timeout=1.0)
                del self._blink_threads[led_name]

            del self._blink_stop_flags[led_name]

        # LEDを消灯（スレッド終了を確実にするため少し待機）
        time.sleep(0.05)
        self.set_led(led_name, False)

    def stop_all_blinks(self):
        """全LEDの点滅を停止"""
        for led_name in list(self._blink_stop_flags.keys()):
            self.stop_blink(led_name)

    def start_all_blink(self, interval: float = 0.3):
        """
        赤・黄・青のLEDを全て同時に点滅（同期）

        Args:
            interval: 点滅間隔（秒）
        """
        # 既存の点滅を停止
        self.stop_all_blinks()

        # 停止フラグを作成
        stop_flag = threading.Event()
        self._blink_stop_flags['all'] = stop_flag

        # 同期点滅スレッド開始
        thread = threading.Thread(
            target=self._all_blink_worker,
            args=(interval, stop_flag),
            daemon=True
        )
        self._blink_threads['all'] = thread
        thread.start()

    def _all_blink_worker(self, interval: float, stop_flag: threading.Event):
        """全ボタンLED同期点滅のワーカー"""
        state = True
        while not stop_flag.is_set():
            # 全てのLEDを同じ状態に設定
            self.set_led('red', state)
            self.set_led('yellow', state)
            self.set_led('blue', state)
            state = not state
            time.sleep(interval)

        # スレッド終了時に全て消灯
        self.set_led('red', False)
        self.set_led('yellow', False)
        self.set_led('blue', False)

    def all_leds_off(self):
        """全LED消灯"""
        self.stop_all_blinks()
        self.led_start.off()
        self.led_red.off()
        self.led_yellow.off()
        self.led_blue.off()

    def all_leds_on(self):
        """全LED点灯"""
        self.stop_all_blinks()
        self.led_start.on()
        self.led_red.on()
        self.led_yellow.on()
        self.led_blue.on()

    def is_button_pressed(self, button_name: str) -> bool:
        """
        指定したボタンが押されているか確認

        Args:
            button_name: 'start', 'red', 'yellow', 'blue'

        Returns:
            True=押されている, False=押されていない
        """
        button_map = {
            'start': self.button_start,
            'red': self.button_red,
            'yellow': self.button_yellow,
            'blue': self.button_blue
        }

        if button_name in button_map:
            return button_map[button_name].is_pressed

        return False

    def wait_for_button(self, button_name: str, timeout: float = None) -> bool:
        """
        指定したボタンが押されるまで待機

        Args:
            button_name: 'start', 'red', 'yellow', 'blue'
            timeout: タイムアウト時間（秒）、Noneは無制限

        Returns:
            True=ボタンが押された, False=タイムアウト
        """
        button_map = {
            'start': self.button_start,
            'red': self.button_red,
            'yellow': self.button_yellow,
            'blue': self.button_blue
        }

        if button_name not in button_map:
            return False

        button = button_map[button_name]

        if timeout is None:
            button.wait_for_press()
            return True
        else:
            return button.wait_for_press(timeout=timeout)

    def cleanup(self):
        """終了処理"""
        self.stop_all_blinks()
        self.all_leds_off()
