from PIL import Image
import os

src = Image.open(r"D:\一个电脑软件\佛教三系日历手机版\icon_source.png").convert("RGBA")
res_root = r"D:\一个电脑软件\佛教三系日历手机版\android\app\src\main\res"

# sizes per density (launcher icon px)
sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

for folder, px in sizes.items():
    d = os.path.join(res_root, folder)
    # ic_launcher.png - full square
    img = src.resize((px, px), Image.LANCZOS)
    img.save(os.path.join(d, "ic_launcher.png"))
    # ic_launcher_round.png - circular mask
    mask = Image.new("L", (px, px), 0)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, px-1, px-1], fill=255)
    round_img = Image.new("RGBA", (px, px), (0,0,0,0))
    round_img.paste(img, (0,0), mask)
    round_img.save(os.path.join(d, "ic_launcher_round.png"))
    # ic_launcher_foreground.png - adaptive icon foreground, scale to 72% with padding
    fg_px = int(px * 1.5)  # foreground canvas is larger
    fg = Image.new("RGBA", (fg_px, fg_px), (0,0,0,0))
    icon = src.resize((int(fg_px*0.66), int(fg_px*0.66)), Image.LANCZOS)
    offset = (fg_px - icon.width) // 2
    fg.paste(icon, (offset, offset), icon)
    fg.save(os.path.join(d, "ic_launcher_foreground.png"))
    print(f"{folder}: {px}x{px} done")

print("all icons generated")
