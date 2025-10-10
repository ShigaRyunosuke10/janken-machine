"""
LEDマトリックスディスプレイモジュール
64x64 RGB LEDマトリックスでの表示を管理

test_display_long.pyで動作確認済みの設定を使用
PILのデフォルトフォント + SetImage() 方式でちらつきなし
"""

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
import time

class MatrixDisplay:
    """LEDマトリックス表示を管理するクラス"""

    def __init__(self):
        # マトリックス設定（test_display_long.pyで動作確認済み）
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.chain_length = 1              # 縦積み構成
        options.parallel = 2                  # 2枚を並列接続（縦方向64x64）
        options.hardware_mapping = 'regular'
        options.disable_hardware_pulsing = True   # ソフトウェアパルス（重要）
        options.gpio_slowdown = 5             # タイミング調整（重要）
        options.brightness = 50
        options.limit_refresh_rate_hz = 120

        # マトリックス初期化
        self.matrix = RGBMatrix(options=options)

        # PILのデフォルトフォントを使用（フォントファイル不要）
        self.font = ImageFont.load_default()

        # 色定義（RGB tuple形式）
        self.COLOR_RED = (255, 0, 0)
        self.COLOR_GREEN = (0, 255, 0)
        self.COLOR_BLUE = (0, 0, 255)
        self.COLOR_YELLOW = (255, 255, 0)
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_CYAN = (0, 255, 255)
        self.COLOR_MAGENTA = (255, 0, 255)
        self.COLOR_ORANGE = (255, 128, 0)
        self.COLOR_BLACK = (0, 0, 0)

    def clear(self):
        """画面クリア"""
        self.matrix.Clear()

    def _create_image(self):
        """新しいPIL Imageを作成"""
        return Image.new('RGB', (self.matrix.width, self.matrix.height))

    def _display_image(self, image):
        """PIL ImageをLEDマトリックスに表示"""
        self.matrix.SetImage(image.convert('RGB'))

    def draw_text(self, text: str, x: int, y: int, color):
        """
        テキストを描画（PIL Image方式 - ちらつき防止）

        Args:
            text: 表示するテキスト
            x: X座標
            y: Y座標
            color: 色（RGB tuple: (r, g, b)）
        """
        image = self._create_image()
        draw = ImageDraw.Draw(image)
        draw.text((x, y), text, font=self.font, fill=color)
        self._display_image(image)

    def draw_multiline_text(self, lines: list):
        """
        複数行テキストを描画（PIL Image方式 - ちらつき防止）

        Args:
            lines: [(text, x, y, color), ...] のリスト
                   color は RGB tuple: (r, g, b)
        """
        image = self._create_image()
        draw = ImageDraw.Draw(image)

        for text, x, y, color in lines:
            draw.text((x, y), text, font=self.font, fill=color)

        self._display_image(image)

    def show_push_start(self):
        """「PUSH START」表示（test_display_long.pyと同じ配置）"""
        self.draw_multiline_text([
            ("PUSH", 10, 16, self.COLOR_GREEN),
            ("START", 8, 40, self.COLOR_CYAN)
        ])

    def show_countdown(self, count: int):
        """
        カウントダウン表示

        Args:
            count: カウント数（3, 2, 1）
        """
        # 大きく中央に表示
        text = str(count)
        self.draw_text(text, 28, 30, self.COLOR_YELLOW)

    def show_choice_prompt(self):
        """「SELECT YOUR HAND」表示"""
        self.draw_multiline_text([
            ("SELECT", 10, 15, self.COLOR_WHITE),
            ("YOUR", 14, 30, self.COLOR_WHITE),
            ("HAND", 14, 45, self.COLOR_WHITE)
        ])

    def show_choice_prompt_with_countdown(self, count: int):
        """
        「SELECT」+ カウントダウン表示

        Args:
            count: カウント数（3, 2, 1）
        """
        count_str = str(count)
        self.draw_multiline_text([
            ("SELECT", 10, 10, self.COLOR_WHITE),
            ("YOUR", 14, 25, self.COLOR_WHITE),
            ("HAND", 14, 40, self.COLOR_WHITE),
            (count_str, 28, 52, self.COLOR_YELLOW)
        ])

    def show_hand(self, hand: str, is_player: bool = True):
        """
        手（グー・チョキ・パー）を表示

        Args:
            hand: 'rock', 'scissors', 'paper'
            is_player: True=プレイヤー, False=CPU
        """
        hand_map = {
            'rock': ("ROCK", self.COLOR_RED),
            'scissors': ("SCIS", self.COLOR_YELLOW),
            'paper': ("PAPER", self.COLOR_BLUE)
        }

        if hand in hand_map:
            text, color = hand_map[hand]
            label = "YOU" if is_player else "CPU"

            self.draw_multiline_text([
                (label, 18, 20, self.COLOR_WHITE),
                (text, 14, 40, color)
            ])

    def show_result(self, result: str):
        """
        結果表示

        Args:
            result: 'win', 'lose', 'draw'
        """
        result_map = {
            'win': [("YOU", 18, 20, self.COLOR_WHITE), ("WIN!", 14, 40, self.COLOR_GREEN)],
            'lose': [("YOU", 18, 20, self.COLOR_WHITE), ("LOSE", 14, 40, self.COLOR_RED)],
            'draw': [("DRAW", 14, 30, self.COLOR_YELLOW)]
        }

        if result in result_map:
            self.draw_multiline_text(result_map[result])

    def show_vs_screen(self, player_hand: str, cpu_hand: str):
        """
        対決画面表示

        Args:
            player_hand: 'rock', 'scissors', 'paper'
            cpu_hand: 'rock', 'scissors', 'paper'
        """
        hand_short = {
            'rock': 'ROCK',
            'scissors': 'SCIS',
            'paper': 'PAPR'
        }

        player_text = hand_short.get(player_hand, '???')
        cpu_text = hand_short.get(cpu_hand, '???')

        self.draw_multiline_text([
            ("YOU", 18, 10, self.COLOR_CYAN),
            (player_text, 14, 22, self.COLOR_WHITE),
            ("VS", 22, 34, self.COLOR_YELLOW),
            (cpu_text, 14, 46, self.COLOR_WHITE)
        ])

    def fill_color(self, r: int, g: int, b: int):
        """
        画面全体を指定色で塗りつぶし（PIL Image方式）

        Args:
            r, g, b: RGB値（0-255）
        """
        image = Image.new('RGB', (self.matrix.width, self.matrix.height), color=(r, g, b))
        self._display_image(image)

    def cleanup(self):
        """終了処理"""
        self.clear()
