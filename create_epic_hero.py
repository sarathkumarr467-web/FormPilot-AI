"""
Epic Photorealistic & Cybernetic AI Document Intelligence Hero Background Generator.
Creates a project-relevant, high-resolution visual for FormPilot AI:
- Official Scholarship Application document with student photo, seal, and clean fields
- Supporting certificates (Income Certificate, Aadhaar Card, Marksheet)
- Laser scanner HUD, glowing AI data nodes, holographic verification stamps
- Multi-layered depth, ambient lighting, and bilingual badges
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_IMG = os.path.join(BASE_DIR, "static", "images", "formpilot-hero.jpg")
FRONTEND_IMG = os.path.join(BASE_DIR, "frontend", "public", "images", "formpilot-hero.jpg")

os.makedirs(os.path.dirname(STATIC_IMG), exist_ok=True)
os.makedirs(os.path.dirname(FRONTEND_IMG), exist_ok=True)

def generate_epic_hero():
    width, height = 1920, 1080
    img = Image.new("RGBA", (width, height), (8, 14, 30, 255))
    draw = ImageDraw.Draw(img)

    # 1. Deep Futuristic Background Gradient
    for y in range(height):
        ratio = y / height
        r = int(7 * (1 - ratio) + 12 * ratio)
        g = int(12 * (1 - ratio) + 20 * ratio)
        b = int(28 * (1 - ratio) + 48 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # 2. Dramatic Ambient Lighting (Cyan glow top right, Violet glow bottom left, Royal Blue center)
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    
    # Top-right Cyan flare
    for rad in range(750, 40, -25):
        alpha = int(45 * (1 - rad / 750))
        gdraw.ellipse([1450 - rad, 250 - rad, 1450 + rad, 250 + rad], fill=(6, 182, 212, alpha))
        
    # Bottom-left Violet/Indigo nebula
    for rad in range(650, 40, -25):
        alpha = int(35 * (1 - rad / 650))
        gdraw.ellipse([350 - rad, 850 - rad, 350 + rad, 850 + rad], fill=(139, 92, 246, alpha))

    # Center-right Document spotlight
    for rad in range(500, 30, -20):
        alpha = int(40 * (1 - rad / 500))
        gdraw.ellipse([1250 - rad, 550 - rad, 1250 + rad, 550 + rad], fill=(37, 99, 235, alpha))

    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # 3. 3D Digital Perspective Desk Grid
    grid_col = (30, 58, 138, 60)
    center_vp = 1150
    horizon_y = 180
    for x in range(-200, width + 400, 80):
        draw.line([(x, height), (center_vp + (x - center_vp) * 0.12, horizon_y)], fill=grid_col, width=1)
    for y in range(horizon_y + 40, height, 38):
        y_ratio = (y - horizon_y) / (height - horizon_y)
        col = (30, 58, 138, int(15 + 75 * y_ratio))
        draw.line([(0, y), (width, y)], fill=col, width=1)

    # 4. Neural Network & Floating AI Data Constellation
    nodes = [
        (100, 200), (280, 140), (450, 260), (220, 380), (140, 520),
        (750, 120), (920, 80), (1050, 160), (880, 240),
        (1580, 140), (1750, 220), (1650, 360), (1820, 440),
        (1480, 850), (1680, 780), (1800, 920), (1350, 960)
    ]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            d = math.hypot(x2 - x1, y2 - y1)
            if d < 220:
                alpha = int(90 * (1 - d / 220))
                draw.line([(x1, y1), (x2, y2)], fill=(6, 182, 212, alpha), width=1)
    for x, y in nodes:
        draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(6, 182, 212, 200))
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255, 255))

    # 5. Background Document 1: Income Certificate (Left Tilted)
    bg_doc1 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d1_draw = ImageDraw.Draw(bg_doc1)
    # Tilted card rectangle
    d1_draw.rounded_rectangle([860, 280, 1280, 860], radius=16, fill=(18, 28, 55, 220), outline=(59, 130, 246, 100), width=1)
    # Header lines
    d1_draw.rounded_rectangle([880, 300, 1260, 350], radius=8, fill=(30, 41, 75, 240))
    d1_draw.line([(910, 320), (1080, 320)], fill=(148, 163, 184, 180), width=6)
    d1_draw.line([(910, 335), (1020, 335)], fill=(100, 116, 139, 150), width=4)
    # Rows
    for ry in range(380, 800, 50):
        d1_draw.line([(890, ry), (1240, ry)], fill=(30, 50, 90, 160), width=1)
        d1_draw.line([(900, ry + 15), (1020, ry + 15)], fill=(148, 163, 184, 120), width=4)
        d1_draw.line([(1060, ry + 15), (1200, ry + 15)], fill=(203, 213, 225, 140), width=4)
    img = Image.alpha_composite(img, bg_doc1)
    draw = ImageDraw.Draw(img)

    # 6. Primary Master Document: Official Post-Matric Scholarship Form
    doc_x, doc_y = 1040, 190
    doc_w, doc_h = 680, 820

    # Glow shadow behind main document
    doc_shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(doc_shadow)
    for spread in range(25, 2, -3):
        alpha = int(35 * (1 - spread / 25))
        s_draw.rounded_rectangle([doc_x - spread, doc_y - spread, doc_x + doc_w + spread, doc_y + doc_h + spread], radius=22, fill=(6, 182, 212, alpha))
    img = Image.alpha_composite(img, doc_shadow)
    draw = ImageDraw.Draw(img)

    # Main Document Paper Body (Slight off-white realistic card styling)
    draw.rounded_rectangle([doc_x, doc_y, doc_x + doc_w, doc_y + doc_h], radius=18, fill=(15, 23, 42, 245), outline=(59, 130, 246, 220), width=2)
    
    # Official Emblem / Header Banner
    draw.rounded_rectangle([doc_x + 20, doc_y + 20, doc_x + doc_w - 20, doc_y + 110], radius=12, fill=(24, 38, 70, 250), outline=(6, 182, 212, 140), width=1)
    
    # Emblem icon
    draw.ellipse([doc_x + 40, doc_y + 35, doc_x + 95, doc_y + 90], fill=(30, 58, 138, 255), outline=(6, 182, 212, 220), width=2)
    draw.polygon([(doc_x + 67, doc_y + 44), (doc_x + 85, doc_y + 78), (doc_x + 50, doc_y + 78)], fill=(6, 182, 212, 255))
    
    # Header Titles
    draw.line([(doc_x + 115, doc_y + 48), (doc_x + 460, doc_y + 48)], fill=(248, 250, 252, 255), width=7)
    draw.line([(doc_x + 115, doc_y + 68), (doc_x + 390, doc_y + 68)], fill=(56, 189, 248, 240), width=4)
    draw.line([(doc_x + 115, doc_y + 85), (doc_x + 320, doc_y + 85)], fill=(148, 163, 184, 200), width=3)

    # Student Photo Card (Top Right)
    photo_x, photo_y = doc_x + doc_w - 125, doc_y + 30
    draw.rounded_rectangle([photo_x, photo_y, photo_x + 90, photo_y + 105], radius=8, fill=(30, 41, 59, 255), outline=(16, 185, 129, 220), width=2)
    # Head and shoulders silhouette
    draw.ellipse([photo_x + 28, photo_y + 20, photo_x + 62, photo_y + 54], fill=(148, 163, 184, 230))
    draw.ellipse([photo_x + 15, photo_y + 60, photo_x + 75, photo_y + 100], fill=(100, 116, 139, 230))
    # Photo "VERIFIED" badge
    draw.rounded_rectangle([photo_x + 8, photo_y + 82, photo_x + 82, photo_y + 100], radius=4, fill=(16, 185, 129, 240))
    draw.line([(photo_x + 22, photo_y + 91), (photo_x + 30, photo_y + 96), (photo_x + 42, photo_y + 86)], fill=(255, 255, 255, 255), width=2)

    # Form Fields Structure
    fields_y = doc_y + 140
    field_data = [
        {"label_w": 180, "val_w": 320, "valid": True},
        {"label_w": 140, "val_w": 280, "valid": True},
        {"label_w": 160, "val_w": 260, "valid": True},
        {"label_w": 210, "val_w": 340, "valid": True},
        {"label_w": 150, "val_w": 240, "valid": True},
        {"label_w": 190, "val_w": 310, "valid": True},
        {"label_w": 170, "val_w": 290, "valid": True},
    ]

    for item in field_data:
        # Label
        draw.line([(doc_x + 35, fields_y), (doc_x + 35 + item["label_w"], fields_y)], fill=(148, 163, 184, 220), width=4)
        # Input Box
        box_y = fields_y + 12
        draw.rounded_rectangle([doc_x + 35, box_y, doc_x + doc_w - 35, box_y + 44], radius=8, fill=(17, 28, 52, 230), outline=(37, 99, 235, 180), width=1)
        # Value text line
        draw.line([(doc_x + 55, box_y + 22), (doc_x + 55 + item["val_w"], box_y + 22)], fill=(241, 245, 249, 255), width=5)
        
        # Emerald checkmark tag
        check_x = doc_x + doc_w - 75
        draw.ellipse([check_x, box_y + 12, check_x + 20, box_y + 32], fill=(16, 185, 129, 240))
        draw.line([(check_x + 5, box_y + 21), (check_x + 9, box_y + 26), (check_x + 16, box_y + 17)], fill=(255, 255, 255, 255), width=2)
        
        fields_y += 74

    # Official Directorate Holographic Stamp (Bottom Right of Document)
    stamp_x, stamp_y = doc_x + doc_w - 170, doc_y + doc_h - 130
    draw.ellipse([stamp_x, stamp_y, stamp_x + 110, stamp_y + 110], fill=(16, 185, 129, 30), outline=(16, 185, 129, 230), width=3)
    draw.ellipse([stamp_x + 8, stamp_y + 8, stamp_x + 102, stamp_y + 102], outline=(16, 185, 129, 140), width=1)
    # Star in center of stamp
    draw.line([(stamp_x + 55, stamp_y + 30), (stamp_x + 55, stamp_y + 80)], fill=(16, 185, 129, 240), width=2)
    draw.line([(stamp_x + 30, stamp_y + 55), (stamp_x + 80, stamp_y + 55)], fill=(16, 185, 129, 240), width=2)
    draw.line([(stamp_x + 38, stamp_y + 38), (stamp_x + 72, stamp_y + 72)], fill=(16, 185, 129, 200), width=2)
    draw.line([(stamp_x + 72, stamp_y + 38), (stamp_x + 38, stamp_y + 72)], fill=(16, 185, 129, 200), width=2)

    # 7. Laser Scanner Beam (Dynamic Scan Effect across Document)
    laser_y = doc_y + 380
    laser_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    l_draw = ImageDraw.Draw(laser_overlay)
    # Core laser line
    l_draw.line([(doc_x - 60, laser_y), (doc_x + doc_w + 60, laser_y)], fill=(6, 182, 212, 255), width=3)
    # Soft glowing halos
    l_draw.line([(doc_x - 80, laser_y), (doc_x + doc_w + 80, laser_y)], fill=(6, 182, 212, 120), width=14)
    l_draw.line([(doc_x - 110, laser_y), (doc_x + doc_w + 110, laser_y)], fill=(6, 182, 212, 50), width=34)
    # Scanning particles
    for px in range(int(doc_x), int(doc_x + doc_w), 40):
        l_draw.ellipse([px - 3, laser_y - 3, px + 3, laser_y + 3], fill=(255, 255, 255, 240))
    img = Image.alpha_composite(img, laser_overlay)
    draw = ImageDraw.Draw(img)

    # 8. High-Tech Holographic HUD Badges floating around document

    # Badge 1: Top Floating "AI Document Intelligence"
    b1_x, b1_y = doc_x - 240, doc_y + 80
    draw.rounded_rectangle([b1_x, b1_y, b1_x + 280, b1_y + 90], radius=14, fill=(15, 23, 42, 245), outline=(6, 182, 212, 220), width=2)
    draw.ellipse([b1_x + 20, b1_y + 24, b1_x + 55, b1_y + 59], fill=(6, 182, 212, 230))
    draw.line([(b1_x + 75, b1_y + 32), (b1_x + 240, b1_y + 32)], fill=(241, 245, 249, 250), width=5)
    draw.line([(b1_x + 75, b1_y + 50), (b1_x + 200, b1_y + 50)], fill=(56, 189, 248, 230), width=3)
    draw.line([(b1_x + 75, b1_y + 66), (b1_x + 160, b1_y + 66)], fill=(148, 163, 184, 180), width=3)

    # Badge 2: Mid Floating "Bilingual Copilot: தமிழ் + EN"
    b2_x, b2_y = doc_x - 280, doc_y + 420
    draw.rounded_rectangle([b2_x, b2_y, b2_x + 310, b2_y + 95], radius=14, fill=(15, 23, 42, 245), outline=(139, 92, 246, 220), width=2)
    draw.ellipse([b2_x + 20, b2_y + 25, b2_x + 60, b2_y + 65], fill=(139, 92, 246, 230))
    draw.line([(b2_x + 80, b2_y + 34), (b2_x + 260, b2_y + 34)], fill=(241, 245, 249, 250), width=5)
    draw.line([(b2_x + 80, b2_y + 54), (b2_x + 230, b2_y + 54)], fill=(192, 132, 252, 230), width=4)
    draw.line([(b2_x + 80, b2_y + 72), (b2_x + 180, b2_y + 72)], fill=(148, 163, 184, 180), width=3)

    # Badge 3: Bottom Right "100% Eligible & DBT Verified"
    b3_x, b3_y = doc_x - 210, doc_y + 700
    draw.rounded_rectangle([b3_x, b3_y, b3_x + 280, b3_y + 90], radius=14, fill=(15, 23, 42, 245), outline=(16, 185, 129, 220), width=2)
    draw.ellipse([b3_x + 20, b3_y + 24, b3_x + 55, b3_y + 59], fill=(16, 185, 129, 240))
    draw.line([(b3_x + 75, b3_y + 32), (b3_x + 230, b3_y + 32)], fill=(241, 245, 249, 250), width=5)
    draw.line([(b3_x + 75, b3_y + 50), (b3_x + 200, b3_y + 50)], fill=(52, 211, 153, 230), width=3)
    draw.line([(b3_x + 75, b3_y + 66), (b3_x + 170, b3_y + 66)], fill=(148, 163, 184, 180), width=3)

    # Data connecting beams from badges to master document
    draw.line([(b1_x + 280, b1_y + 45), (doc_x, doc_y + 120)], fill=(6, 182, 212, 160), width=1)
    draw.line([(b2_x + 310, b2_y + 48), (doc_x, doc_y + 440)], fill=(139, 92, 246, 160), width=1)
    draw.line([(b3_x + 280, b3_y + 45), (doc_x, doc_y + 720)], fill=(16, 185, 129, 160), width=1)

    # Convert to RGB and Save with top quality
    final_img = img.convert("RGB")
    final_img.save(STATIC_IMG, quality=96)
    final_img.save(FRONTEND_IMG, quality=96)
    print(f"Created upgraded hero image -> {STATIC_IMG} & {FRONTEND_IMG}")

if __name__ == "__main__":
    generate_epic_hero()
