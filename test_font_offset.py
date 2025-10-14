#!/usr/bin/env python3
"""
フォントのオフセットとバウンディングボックスを調査
"""

from PIL import Image, ImageDraw, ImageFont

# Noto Sans CJK JP フォント読み込み
font = ImageFont.truetype(
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    12,
    index=0
)

# テスト文字列
test_texts = ["じゃんけん", "ゲーム", "あなた", "1", "A"]

print("=" * 60)
print("フォントオフセット調査")
print("=" * 60)

for text in test_texts:
    # getbbox: (left, top, right, bottom)
    bbox = font.getbbox(text)
    print(f"\nテキスト: '{text}'")
    print(f"  bbox: {bbox}")
    print(f"  left={bbox[0]}, top={bbox[1]}, right={bbox[2]}, bottom={bbox[3]}")
    print(f"  幅: {bbox[2] - bbox[0]}px")
    print(f"  高さ: {bbox[3] - bbox[1]}px")
    print(f"  上部オフセット（top）: {bbox[1]}px")

# 実際の描画位置を確認
print("\n" + "=" * 60)
print("実際の描画位置確認")
print("=" * 60)

image = Image.new('RGB', (64, 64), color=(0, 0, 0))
draw = ImageDraw.Draw(image)

# y=0で描画した場合
draw.text((0, 0), "じゃんけん", font=font, fill=(255, 255, 255))

# ピクセルデータから実際の描画開始位置を調べる
pixels = image.load()
first_pixel_y = None
for y in range(64):
    for x in range(64):
        if pixels[x, y] != (0, 0, 0):
            first_pixel_y = y
            break
    if first_pixel_y is not None:
        break

print(f"\ny=0で描画した場合の実際の描画開始Y座標: {first_pixel_y}")
print(f"→ オフセット: {first_pixel_y}px")

# anchor='lt' (left-top) を使った場合
image2 = Image.new('RGB', (64, 64), color=(0, 0, 0))
draw2 = ImageDraw.Draw(image2)
draw2.text((0, 0), "じゃんけん", font=font, fill=(255, 255, 255), anchor='lt')

pixels2 = image2.load()
first_pixel_y2 = None
for y in range(64):
    for x in range(64):
        if pixels2[x, y] != (0, 0, 0):
            first_pixel_y2 = y
            break
    if first_pixel_y2 is not None:
        break

print(f"\nanchor='lt'でy=0で描画した場合の実際の描画開始Y座標: {first_pixel_y2}")
print(f"→ オフセット: {first_pixel_y2}px")

print("\n" + "=" * 60)
print("推奨修正量")
print("=" * 60)
if first_pixel_y is not None:
    print(f"現在のy座標から -{first_pixel_y}px すれば、y=0から描画開始されます")
    print(f"例: y=0を指定 → 実際はy={first_pixel_y}から描画")
    print(f"    y={-first_pixel_y}を指定 → 実際はy=0から描画")
