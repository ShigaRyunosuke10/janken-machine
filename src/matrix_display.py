"""
LEDマトリックスディスプレイモジュール
64x64 RGB LEDマトリックスでの表示を管理
"""

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

class MatrixDisplay:
    """LEDマトリックス表示を管理するクラス"""

    def __init__(self, font_path="/home/janken/rpi-rgb-led-matrix/fonts/7x13.bdf"):
        # マトリックス設定
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.chain_length = 2
        options.parallel = 1
        options.hardware_mapping = 'regular'
        options.gpio_slowdown = 4

        # マトリックス初期化
        self.matrix = RGBMatrix(options=options)

        # フォント読み込み
        self.font = graphics.Font()
        self.font.LoadFont(font_path)

        # 色定義
        self.COLOR_RED = graphics.Color(255, 0, 0)
        self.COLOR_GREEN = graphics.Color(0, 255, 0)
        self.COLOR_BLUE = graphics.Color(0, 0, 255)
        self.COLOR_YELLOW = graphics.Color(255, 255, 0)
        self.COLOR_WHITE = graphics.Color(255, 255, 255)
        self.COLOR_CYAN = graphics.Color(0, 255, 255)
        self.COLOR_MAGENTA = graphics.Color(255, 0, 255)
        self.COLOR_ORANGE = graphics.Color(255, 128, 0)

    def clear(self):
        """画面クリア"""
        self.matrix.Clear()

    def draw_text(self, text: str, x: int, y: int, color):
        """
        テキストを描画

        Args:
            text: 表示するテキスト
            x: X座標
            y: Y座標
            color: 色（graphics.Color）
        """
        canvas = self.matrix.CreateFrameCanvas()
        graphics.DrawText(canvas, self.font, x, y, color, text)
        self.matrix.SwapOnVSync(canvas)

    def draw_text_centered(self, text: str, y: int, color):
        """
        テキストを中央寄せで描画

        Args:
            text: 表示するテキスト
            y: Y座標
            color: 色（graphics.Color）
        """
        text_width = len(text) * 7  # 7x13フォントの幅は約7px
        x = (64 - text_width) // 2
        self.draw_text(text, x, y, color)

    def draw_multiline_text(self, lines: list):
        """
        複数行テキストを描画

        Args:
            lines: [(text, color, y_pos), ...] のリスト
        """
        canvas = self.matrix.CreateFrameCanvas()
        canvas.Clear()

        for text, color, y_pos in lines:
            text_width = len(text) * 7
            x_pos = (64 - text_width) // 2
            graphics.DrawText(canvas, self.font, x_pos, y_pos, color, text)

        self.matrix.SwapOnVSync(canvas)

    def show_push_start(self):
        """「PUSH START」表示"""
        self.draw_multiline_text([
            ("PUSH", self.COLOR_GREEN, 20),
            ("START", self.COLOR_CYAN, 40)
        ])

    def show_countdown(self, count: int):
        """
        カウントダウン表示

        Args:
            count: カウント数（3, 2, 1）
        """
        self.draw_text_centered(str(count), 35, self.COLOR_YELLOW)

    def show_choice_prompt(self):
        """「SELECT」表示"""
        self.draw_multiline_text([
            ("SELECT", self.COLOR_WHITE, 25),
            ("YOUR", self.COLOR_WHITE, 40),
            ("HAND", self.COLOR_WHITE, 55)
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
            'scissors': ("SCISSORS", self.COLOR_YELLOW),
            'paper': ("PAPER", self.COLOR_BLUE)
        }

        if hand in hand_map:
            text, color = hand_map[hand]
            label = "YOU" if is_player else "CPU"

            self.draw_multiline_text([
                (label, self.COLOR_WHITE, 20),
                (text, color, 40)
            ])

    def show_result(self, result: str):
        """
        結果表示

        Args:
            result: 'win', 'lose', 'draw'
        """
        result_map = {
            'win': ("YOU", "WIN!", self.COLOR_GREEN),
            'lose': ("YOU", "LOSE", self.COLOR_RED),
            'draw': ("", "DRAW", self.COLOR_YELLOW)
        }

        if result in result_map:
            line1, line2, color = result_map[result]

            if line1:
                self.draw_multiline_text([
                    (line1, self.COLOR_WHITE, 25),
                    (line2, color, 45)
                ])
            else:
                self.draw_text_centered(line2, 35, color)

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
            ("YOU", self.COLOR_CYAN, 15),
            (player_text, self.COLOR_WHITE, 28),
            ("VS", self.COLOR_YELLOW, 41),
            (cpu_text, self.COLOR_WHITE, 54)
        ])

    def fill_color(self, r: int, g: int, b: int):
        """
        画面全体を指定色で塗りつぶし

        Args:
            r, g, b: RGB値（0-255）
        """
        canvas = self.matrix.CreateFrameCanvas()
        for x in range(64):
            for y in range(64):
                canvas.SetPixel(x, y, r, g, b)
        self.matrix.SwapOnVSync(canvas)

    def cleanup(self):
        """終了処理"""
        self.clear()
