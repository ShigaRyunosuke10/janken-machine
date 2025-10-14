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
        draw.text((x, y), text, font=self.font, fill=color, anchor='lt')
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

        # 上下の装飾線を描画
        draw.line([(0, 0), (63, 0)], fill=self.COLOR_CYAN, width=1)  # 上の線
        draw.line([(0, 63), (63, 63)], fill=self.COLOR_CYAN, width=1)  # 下の線

        for text, x, y, color in lines:
            draw.text((x, y), text, font=self.font, fill=color, anchor='lt')

        self._display_image(image)

    def show_push_start(self):
        """「じゃんけんゲーム スタートを押してね」表示"""
        self.draw_multiline_text([
            ("じゃんけん", 2, 4, self.COLOR_GREEN),
            ("ゲーム", 16, 18, self.COLOR_GREEN),
            ("スタートを", 2, 36, self.COLOR_CYAN),
            ("おしてね", 8, 50, self.COLOR_CYAN)
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
        「手を えらんで」+ カウントダウン表示

        Args:
            count: カウント数（5, 4, 3, 2, 1）
        """
        count_str = str(count)
        # 数字は1桁なので約7px、中央は(64-7)/2≈28
        self.draw_multiline_text([
            ("手を", 20, 6, self.COLOR_WHITE),
            ("えらんで", 8, 20, self.COLOR_WHITE),
            (count_str, 28, 42, self.COLOR_YELLOW)
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
            if is_player:
                label = "あなた"
                label_color = self.COLOR_CYAN
            else:
                label = "わたし"
                label_color = self.COLOR_MAGENTA

            # 手の位置: グー・パー(2文字)は x=20、チョキ(3文字)は x=14 で「あなた」と揃える
            if text == "チョキ":
                hand_x = 14
            else:
                hand_x = 20

            self.draw_multiline_text([
                (label, 14, 8, label_color),
                (text, hand_x, 42, color)
            ])

    def show_result(self, result: str, win_streak: int = 0):
        """
        結果表示

        Args:
            result: 'win', 'lose', 'draw'
            win_streak: 連勝数（勝った時のみ表示）
        """
        if result == 'win' and win_streak > 0:
            streak_text = f"{win_streak}連勝中"
            result_map = {
                'win': [("あなたの", 8, 6, self.COLOR_WHITE), ("かち", 20, 20, self.COLOR_GREEN), (streak_text, 8, 36, self.COLOR_YELLOW)]
            }
        else:
            result_map = {
                'win': [("あなたの", 8, 20, self.COLOR_WHITE), ("かち", 20, 32, self.COLOR_GREEN)],
                'lose': [("あなたの", 8, 20, self.COLOR_WHITE), ("まけ", 20, 32, self.COLOR_RED)],
                'draw': [("あいこ", 14, 26, self.COLOR_YELLOW)]
            }

        if result in result_map:
            self.draw_multiline_text(result_map[result])

    def show_no_selection(self):
        """「時間切れ」表示"""
        self.draw_multiline_text([
            ("じかん", 14, 8, self.COLOR_YELLOW),
            ("きれ", 20, 42, self.COLOR_YELLOW)
        ])

    def show_continue_prompt(self, win_streak: int = 0, countdown: int = 5):
        """「続きをやる？」表示

        Args:
            win_streak: 現在の連勝数
            countdown: 残り時間（秒）
        """
        countdown_str = str(countdown)
        if win_streak > 0:
            streak_text = f"{win_streak}連勝中"
            self.draw_multiline_text([
                (streak_text, 12, 6, self.COLOR_YELLOW),
                ("つづきを", 6, 20, self.COLOR_WHITE),
                ("やる？", 10, 38, self.COLOR_WHITE),
                (countdown_str, 28, 52, self.COLOR_CYAN)
            ])
        else:
            self.draw_multiline_text([
                ("つづきを", 6, 14, self.COLOR_WHITE),
                ("やる？", 10, 38, self.COLOR_WHITE),
                (countdown_str, 28, 52, self.COLOR_CYAN)
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

        # プレイヤーの手の位置: チョキは x=14、グー・パーは x=20
        player_x = 14 if player_text == "チョキ" else 20
        # CPUの手の位置: チョキは x=14、グー・パーは x=20
        cpu_x = 14 if cpu_text == "チョキ" else 20

        self.draw_multiline_text([
            ("あなた", 14, 4, self.COLOR_CYAN),
            (player_text, player_x, 18, self.COLOR_WHITE),
            ("わたし", 14, 36, self.COLOR_MAGENTA),
            (cpu_text, cpu_x, 50, self.COLOR_WHITE)
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
