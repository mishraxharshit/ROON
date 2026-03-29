"""
Generate app icon for Windows (.ico) and Mac (.icns)
Run this before building the app.
"""
from PIL import Image, ImageDraw, ImageFont
import os, subprocess, shutil

def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    s, p = size, max(1, size//12)
    d.rounded_rectangle([p, p//2, s-p, s-p//2],
                         radius=max(2,s//14), fill=(255,252,246),
                         outline=(200,188,170), width=max(1,s//80))
    fold = max(4, s//5)
    fx = s-p-fold; fy = p//2+fold
    d.polygon([(fx,p//2+1),(s-p-1,p//2+1),(s-p-1,fy)], fill=(232,220,200))
    d.line([(fx,p//2+1),(fx,fy),(s-p-1,fy)], fill=(185,170,148), width=max(1,s//80))
    bw = max(2,s//9); bh = max(4,s//3); by = s//4
    d.rounded_rectangle([0,by,bw,by+bh], radius=max(1,bw//2), fill=(0,120,212))
    lc=(175,162,140); lw=max(1,s//52)
    lx0=p+s//7; lx1=s-p-s//9; ly=fy+max(3,s//7); gap=max(3,s//8)
    for i in range(5):
        y=ly+i*gap
        if y<s-p-gap:
            d.line([(lx0,y),(fx-s//8 if i==0 else lx1,y)], fill=lc, width=lw)
    if size >= 48:
        try:
            fs = max(7, size//8)
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fs)
            tw = d.textlength("PDF", font=font)
            tx=(s-tw)//2; ty=s-p//2-fs-max(2,s//16)
            d.text((tx,ty), "PDF", fill=(0,100,190), font=font)
        except: pass
    return img

def main():
    os.makedirs("assets", exist_ok=True)

    # Windows ICO
    sizes = [16,32,48,64,128,256]
    images = [draw_icon(s) for s in sizes]
    images[0].save("assets/app.ico", format="ICO",
                   sizes=[(s,s) for s in sizes],
                   append_images=images[1:])
    print("Windows icon: assets/app.ico")

    # PNG versions
    draw_icon(256).save("assets/app_icon.png")
    draw_icon(512).save("assets/app_512.png")
    print("PNG icons saved")

    # Mac ICNS (using iconutil on Mac, or just PNG on other platforms)
    try:
        iconset_dir = "assets/AppIcon.iconset"
        os.makedirs(iconset_dir, exist_ok=True)
        mac_sizes = [(16,1),(16,2),(32,1),(32,2),(64,1),(64,2),
                     (128,1),(128,2),(256,1),(256,2),(512,1),(512,2)]
        for sz, scale in mac_sizes:
            px = sz * scale
            img = draw_icon(px)
            suffix = "" if scale==1 else "@2x"
            img.save(f"{iconset_dir}/icon_{sz}x{sz}{suffix}.png")
        result = subprocess.run(
            ["iconutil", "-c", "icns", iconset_dir,
             "-o", "assets/app.icns"],
            capture_output=True)
        if result.returncode == 0:
            print("Mac icon: assets/app.icns")
            shutil.rmtree(iconset_dir)
        else:
            # Fallback: copy PNG as icns placeholder
            import shutil
            shutil.copy("assets/app_512.png", "assets/app.icns")
            print("Mac icon (PNG fallback): assets/app.icns")
    except FileNotFoundError:
        # Not on Mac - save PNG, GitHub Actions (mac runner) will use it
        print("Mac ICNS: skipped (not on macOS, will be generated in CI)")

if __name__ == "__main__":
    main()
    print("Done!")
