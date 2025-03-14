from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with transparency
icon_size = 256
img = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw a red rectangle for PDF
background_color = (255, 74, 54)  # Red color
draw.rectangle([40, 20, 216, 236], fill=background_color)

# Add white "PDF" text
try:
    font = ImageFont.truetype("arial.ttf", 80)
except:
    font = ImageFont.load_default()
draw.text((65, 90), "PDF", fill="white", font=font)

# Save as ICO file
img.save('icon.ico', format='ICO', sizes=[(256, 256)])