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

        # 日本語フォント（Noto Sans CJK JP）12×12ピクセル
        try:
            self.font = ImageFont.truetype(
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                12,
                index=0  # Noto Sans CJK JP
            )
        except Exception as e:
            print(f"Warning: Could not load Japanese font: {e}")
            print("Falling back to default font")
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
        """「スタート」表示"""
        self.draw_multiline_text([
            ("じゃんけん", 4, 16, self.COLOR_GREEN),
            ("スタート", 4, 38, self.COLOR_CYAN)
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
        """「手を選んで」表示"""
        self.draw_multiline_text([
            ("手を", 18, 18, self.COLOR_WHITE),
            ("えらんで", 6, 38, self.COLOR_WHITE)
        ])

    def show_choice_prompt_with_countdown(self, count: int):
        """
        「えらんで」+ カウントダウン表示

        Args:
            count: カウント数（5, 4, 3, 2, 1）
        """
        count_str = str(count)
        self.draw_multiline_text([
            ("えらんで", 6, 16, self.COLOR_WHITE),
            (count_str, 26, 38, self.COLOR_YELLOW)
        ])

    def show_hand(self, hand: str, is_player: bool = True):
        """
        手（グー・チョキ・パー）を表示

        Args:
            hand: 'rock', 'scissors', 'paper'
            is_player: True=プレイヤー, False=CPU
        """
        hand_map = {
            'rock': ("グー", self.COLOR_RED),
            'scissors': ("チョキ", self.COLOR_YELLOW),
            'paper': ("パー", self.COLOR_BLUE)
        }

        if hand in hand_map:
            text, color = hand_map[hand]
            label = "あなた" if is_player else "CPU"

            self.draw_multiline_text([
                (label, 12, 20, self.COLOR_WHITE),
                (text, 16, 40, color)
            ])

    def show_result(self, result: str):
        """
        結果表示

        Args:
            result: 'win', 'lose', 'draw'
        """
        result_map = {
            'win': [("あなた", 8, 16, self.COLOR_WHITE), ("かち！", 8, 38, self.COLOR_GREEN)],
            'lose': [("あなた", 8, 16, self.COLOR_WHITE), ("まけ", 12, 38, self.COLOR_RED)],
            'draw': [("あいこ", 10, 26, self.COLOR_YELLOW)]
        }

        if result in result_map:
            self.draw_multiline_text(result_map[result])

    def show_no_selection(self):
        """「時間切れ」表示"""
        self.draw_multiline_text([
            ("じかん", 10, 18, self.COLOR_YELLOW),
            ("きれ", 14, 38, self.COLOR_YELLOW)
        ])

    def show_vs_screen(self, player_hand: str, cpu_hand: str):
        """
        対決画面表示

        Args:
            player_hand: 'rock', 'scissors', 'paper'
            cpu_hand: 'rock', 'scissors', 'paper'
        """
        hand_map = {
            'rock': 'グー',
            'scissors': 'チョキ',
            'paper': 'パー'
        }

        player_text = hand_map.get(player_hand, '???')
        cpu_text = hand_map.get(cpu_hand, '???')

        self.draw_multiline_text([
            ("あなた", 12, 6, self.COLOR_CYAN),
            (player_text, 16, 20, self.COLOR_WHITE),
            ("VS", 22, 34, self.COLOR_YELLOW),
            (cpu_text, 16, 48, self.COLOR_WHITE)
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
