"""
Asset Generation Script for FormPilot AI.
Creates high-resolution, professional, project-relevant visuals:
1. formpilot-hero.jpg: High-tech AI document intelligence, digital forms, validation nodes, Tamil+English badges.
2. formpilot-logo.png: Crisp vector-styled modern logo with AI pilot wings + document checkmark.
3. module illustrations for Form Analyzer, Create & Fill, Explain Filled Form, Document Center, Tracker.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "images")
FRONTEND_IMG_DIR = os.path.join(BASE_DIR, "frontend", "public", "images")

os.makedirs(STATIC_IMG_DIR, exist_ok=True)
os.makedirs(FRONTEND_IMG_DIR, exist_ok=True)

def create_hero_image():
    width, height = 1920, 1080
    img = Image.new("RGBA", (width, height), (10, 17, 40, 255))
    draw = ImageDraw.Draw(img)
    
    # 1. Background Gradient (Deep Navy to Royal Blue to Dark Slate)
    for y in range(height):
        ratio = y / height
        r = int(10 * (1 - ratio) + 15 * ratio)
        g = int(17 * (1 - ratio) + 23 * ratio)
        b = int(40 * (1 - ratio) + 65 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        
    # 2. Glowing Radial Ambient Lights (Cyan glow at top right, Violet glow at bottom left)
    glow_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    
    # Cyan ambient top right
    for rad in range(600, 50, -25):
        alpha = int(35 * (1 - rad / 600))
        glow_draw.ellipse(
            [1400 - rad, 350 - rad, 1400 + rad, 350 + rad],
            fill=(6, 182, 212, alpha)
        )
    # Violet ambient bottom left
    for rad in range(500, 50, -25):
        alpha = int(30 * (1 - rad / 500))
        glow_draw.ellipse(
            [400 - rad, 750 - rad, 400 + rad, 750 + rad],
            fill=(139, 92, 246, alpha)
        )
    # Royal blue central pulse
    for rad in range(450, 40, -20):
        alpha = int(40 * (1 - rad / 450))
        glow_draw.ellipse(
            [960 - rad, 500 - rad, 960 + rad, 500 + rad],
            fill=(37, 99, 235, alpha)
        )
    
    img = Image.alpha_composite(img, glow_overlay)
    draw = ImageDraw.Draw(img)
    
    # 3. High-tech Perspective Grid Lines (Digital Matrix Floor)
    grid_color = (30, 58, 138, 70)
    center_x = 960
    vanishing_y = 300
    for x in range(0, width + 200, 100):
        draw.line([(x, height), (center_x + (x - center_x) * 0.15, vanishing_y + 200)], fill=grid_color, width=1)
    for y in range(520, height, 45):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # 4. Neural Network / Data Flow Particles & Curves
    node_coords = [
        (250, 280), (420, 200), (600, 320), (320, 450),
        (1300, 220), (1500, 310), (1680, 240), (1420, 430), (1620, 520),
        (850, 220), (1070, 210), (780, 350), (1140, 340)
    ]
    # Connect nearby nodes
    for i in range(len(node_coords)):
        for j in range(i + 1, len(node_coords)):
            x1, y1 = node_coords[i]
            x2, y2 = node_coords[j]
            dist = math.hypot(x2 - x1, y2 - y1)
            if dist < 260:
                alpha = int(120 * (1 - dist / 260))
                draw.line([(x1, y1), (x2, y2)], fill=(6, 182, 212, alpha), width=1)
                
    for x, y in node_coords:
        draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(6, 182, 212, 220))
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255, 255))

    # 5. Central High-Tech Holographic Document Card (Smart Form)
    doc_w, doc_h = 580, 720
    doc_x, doc_y = (width - doc_w) // 2 + 180, 220
    
    # Document drop glow
    doc_glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(doc_glow)
    d_draw.rounded_rectangle([doc_x - 15, doc_y - 15, doc_x + doc_w + 15, doc_y + doc_h + 15], radius=24, fill=(6, 182, 212, 45))
    d_draw.rounded_rectangle([doc_x - 5, doc_y - 5, doc_x + doc_w + 5, doc_y + doc_h + 5], radius=20, fill=(37, 99, 235, 75))
    img = Image.alpha_composite(img, doc_glow)
    draw = ImageDraw.Draw(img)
    
    # Document Glass Body
    draw.rounded_rectangle([doc_x, doc_y, doc_x + doc_w, doc_y + doc_h], radius=18, fill=(15, 23, 42, 235), outline=(59, 130, 246, 200), width=2)
    
    # Document Header Bar
    draw.rounded_rectangle([doc_x + 20, doc_y + 20, doc_x + doc_w - 20, doc_y + 85], radius=10, fill=(30, 41, 59, 240), outline=(6, 182, 212, 120), width=1)
    draw.ellipse([doc_x + 40, doc_y + 38, doc_x + 65, doc_y + 63], fill=(37, 99, 235, 255))
    # Checkmark inside header icon
    draw.line([(doc_x + 47, doc_y + 51), (doc_x + 51, doc_y + 56), (doc_x + 59, doc_y + 45)], fill=(255, 255, 255, 255), width=2)
    
    # Document Header lines
    draw.line([(doc_x + 80, doc_y + 44), (doc_x + 280, doc_y + 44)], fill=(241, 245, 249, 230), width=6)
    draw.line([(doc_x + 80, doc_y + 60), (doc_x + 210, doc_y + 60)], fill=(148, 163, 184, 180), width=3)
    
    # AI Verified Badge on Document
    draw.rounded_rectangle([doc_x + doc_w - 150, doc_y + 35, doc_x + doc_w - 35, doc_y + 70], radius=8, fill=(16, 185, 129, 40), outline=(16, 185, 129, 220), width=1)
    
    # Document Form Fields (Simulated Smart Inputs with AI Guidance)
    fields = [
        {"label_w": 140, "val_w": 260, "status": "verified"},
        {"label_w": 180, "val_w": 320, "status": "verified"},
        {"label_w": 110, "val_w": 220, "status": "ai_filled"},
        {"label_w": 160, "val_w": 300, "status": "verified"},
        {"label_w": 130, "val_w": 240, "status": "ai_filled"},
        {"label_w": 200, "val_w": 340, "status": "verified"},
    ]
    
    f_y = doc_y + 115
    for f in fields:
        # Label
        draw.line([(doc_x + 35, f_y), (doc_x + 35 + f["label_w"], f_y)], fill=(148, 163, 184, 200), width=4)
        # Input Box
        box_y = f_y + 12
        border_col = (16, 185, 129, 200) if f["status"] == "verified" else (6, 182, 212, 220)
        bg_col = (15, 30, 50, 220)
        draw.rounded_rectangle([doc_x + 35, box_y, doc_x + doc_w - 35, box_y + 42], radius=8, fill=bg_col, outline=border_col, width=1)
        # Value Line
        draw.line([(doc_x + 55, box_y + 21), (doc_x + 55 + f["val_w"], box_y + 21)], fill=(226, 232, 240, 240), width=5)
        # Check / AI Badge icon
        if f["status"] == "verified":
            draw.ellipse([doc_x + doc_w - 70, box_y + 13, doc_x + doc_w - 52, box_y + 31], fill=(16, 185, 129, 230))
            draw.line([(doc_x + doc_w - 65, box_y + 22), (doc_x + doc_w - 63, box_y + 26), (doc_x + doc_w - 57, box_y + 18)], fill=(255, 255, 255, 255), width=2)
        else:
            draw.ellipse([doc_x + doc_w - 70, box_y + 13, doc_x + doc_w - 52, box_y + 31], fill=(139, 92, 246, 230))
        f_y += 75

    # Document Scanning Laser Line
    laser_y = doc_y + 320
    draw.line([(doc_x - 40, laser_y), (doc_x + doc_w + 40, laser_y)], fill=(6, 182, 212, 255), width=3)
    # Laser Glow
    laser_glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    lg_draw = ImageDraw.Draw(laser_glow)
    lg_draw.line([(doc_x - 60, laser_y), (doc_x + doc_w + 60, laser_y)], fill=(6, 182, 212, 100), width=12)
    lg_draw.line([(doc_x - 80, laser_y), (doc_x + doc_w + 80, laser_y)], fill=(6, 182, 212, 40), width=28)
    img = Image.alpha_composite(img, laser_glow)
    draw = ImageDraw.Draw(img)

    # 6. Floating Smart Feature Badges (Orbiting AI Cards)
    # Badge 1: Top Left - AI Field Extraction (99.4% Accuracy)
    b1_x, b1_y = doc_x - 220, doc_y + 60
    draw.rounded_rectangle([b1_x, b1_y, b1_x + 260, b1_y + 85], radius=14, fill=(15, 23, 42, 245), outline=(6, 182, 212, 220), width=2)
    draw.ellipse([b1_x + 18, b1_y + 20, b1_x + 48, b1_y + 50], fill=(6, 182, 212, 240))
    draw.line([(b1_x + 60, b1_y + 26), (b1_x + 210, b1_y + 26)], fill=(255, 255, 255, 240), width=5)
    draw.line([(b1_x + 60, b1_y + 44), (b1_x + 160, b1_y + 44)], fill=(6, 182, 212, 220), width=3)
    draw.line([(b1_x + 60, b1_y + 60), (b1_x + 180, b1_y + 60)], fill=(148, 163, 184, 180), width=3)

    # Badge 2: Bottom Left - Bilingual Tamil + English Engine
    b2_x, b2_y = doc_x - 260, doc_y + 360
    draw.rounded_rectangle([b2_x, b2_y, b2_x + 280, b2_y + 90], radius=14, fill=(15, 23, 42, 245), outline=(139, 92, 246, 220), width=2)
    draw.ellipse([b2_x + 20, b2_y + 25, b2_x + 55, b2_y + 60], fill=(139, 92, 246, 240))
    draw.line([(b2_x + 70, b2_y + 30), (b2_x + 240, b2_y + 30)], fill=(255, 255, 255, 240), width=5)
    draw.line([(b2_x + 70, b2_y + 50), (b2_x + 210, b2_y + 50)], fill=(167, 139, 250, 220), width=4)
    draw.line([(b2_x + 70, b2_y + 68), (b2_x + 160, b2_y + 68)], fill=(148, 163, 184, 180), width=3)

    # Badge 3: Right Bottom - Zero-Error Form Verification
    b3_x, b3_y = doc_x + doc_w + 30, doc_y + 480
    draw.rounded_rectangle([b3_x, b3_y, b3_x + 260, b3_y + 85], radius=14, fill=(15, 23, 42, 245), outline=(16, 185, 129, 220), width=2)
    draw.ellipse([b3_x + 18, b3_y + 20, b3_x + 48, b3_y + 50], fill=(16, 185, 129, 240))
    draw.line([(b3_x + 60, b3_y + 26), (b3_x + 220, b3_y + 26)], fill=(255, 255, 255, 240), width=5)
    draw.line([(b3_x + 60, b3_y + 44), (b3_x + 170, b3_y + 44)], fill=(52, 211, 153, 220), width=3)
    draw.line([(b3_x + 60, b3_y + 60), (b3_x + 190, b3_y + 60)], fill=(148, 163, 184, 180), width=3)

    # Connection Beams from badges to document
    draw.line([(b1_x + 260, b1_y + 40), (doc_x, doc_y + 90)], fill=(6, 182, 212, 140), width=1)
    draw.line([(b2_x + 280, b2_y + 45), (doc_x, doc_y + 380)], fill=(139, 92, 246, 140), width=1)
    draw.line([(b3_x, b3_y + 42), (doc_x + doc_w, doc_y + 500)], fill=(16, 185, 129, 140), width=1)

    # Convert to RGB and save
    final_img = img.convert("RGB")
    hero_static_path = os.path.join(STATIC_IMG_DIR, "formpilot-hero.jpg")
    hero_frontend_path = os.path.join(FRONTEND_IMG_DIR, "formpilot-hero.jpg")
    final_img.save(hero_static_path, quality=95)
    final_img.save(hero_frontend_path, quality=95)
    print(f"Created hero image -> {hero_static_path}")

def create_logo():
    size = (512, 512)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer Rounded Shield with Gradient feel
    draw.rounded_rectangle([24, 24, 488, 488], radius=110, fill=(15, 23, 42, 255), outline=(37, 99, 235, 255), width=8)
    
    # Radial glow behind emblem
    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    for rad in range(180, 20, -10):
        alpha = int(45 * (1 - rad / 180))
        g_draw.ellipse([256 - rad, 256 - rad, 256 + rad, 256 + rad], fill=(6, 182, 212, alpha))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)
    
    # Modern Digital Document Folded Sheet in Center
    doc_points = [
        (150, 100), (320, 100), (380, 160), (380, 410), (150, 410)
    ]
    draw.polygon(doc_points, fill=(30, 58, 138, 230), outline=(6, 182, 212, 255))
    # Corner fold
    draw.polygon([(320, 100), (380, 160), (320, 160)], fill=(59, 130, 246, 255), outline=(6, 182, 212, 255))
    
    # Document Lines
    draw.line([(190, 170), (300, 170)], fill=(226, 232, 240, 240), width=10)
    draw.line([(190, 210), (340, 210)], fill=(148, 163, 184, 200), width=8)
    draw.line([(190, 250), (320, 250)], fill=(148, 163, 184, 200), width=8)
    draw.line([(190, 290), (280, 290)], fill=(148, 163, 184, 200), width=8)
    
    # FormPilot AI Navigation Wings (Pilot motif)
    # Left Wing
    draw.polygon([(90, 290), (160, 250), (150, 340)], fill=(6, 182, 212, 240), outline=(255, 255, 255, 200))
    # Right Wing
    draw.polygon([(422, 290), (352, 250), (362, 340)], fill=(139, 92, 246, 240), outline=(255, 255, 255, 200))
    
    # Floating Emerald Green Verified Badge Checkmark at bottom right of document
    draw.ellipse([310, 330, 430, 450], fill=(16, 185, 129, 255), outline=(255, 255, 255, 255), width=6)
    # Checkmark inside badge
    draw.line([(340, 390), (365, 415), (405, 365)], fill=(255, 255, 255, 255), width=10)
    
    logo_static_path = os.path.join(STATIC_IMG_DIR, "formpilot-logo.png")
    logo_frontend_path = os.path.join(FRONTEND_IMG_DIR, "formpilot-logo.png")
    img.save(logo_static_path, "PNG")
    img.save(logo_frontend_path, "PNG")
    print(f"Created logo -> {logo_static_path}")

if __name__ == "__main__":
    create_hero_image()
    create_logo()
