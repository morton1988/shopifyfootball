from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter
import os
import io
import uuid

app = Flask(__name__)

# Font setup
FONT_PATH = "static/fonts/RadikalTrial-Bold.otf"
FALLBACK_FONT = "static/fonts/arial.ttf"

# Team data with updated relative paths
TEAMS = {
    "Arsenal": {"template_path": "static/teams/arsenal no name.jpg", "text_color": "#DEDEE0", "x": 1680, "y": 820},
    "Aston Villa": {"template_path": "static/teams/ASTON VILLA NO NAME BOARDER.jpg", "text_color": "#C6C6C6", "x": 1648, "y": 795},
    "Watford": {"template_path": "static/teams/WATFORD no name.jpg", "text_color": "#000000", "x": 1735, "y": 820},
    "Brentford": {"template_path": "static/teams/brentford NO NAME.jpg", "text_color": "#100E0F", "x": 1825, "y": 820},
    "Brighton": {"template_path": "static/teams/brighton NO NAME.jpg", "text_color": "#939393", "x": 1715, "y": 820},
    "Burnley": {"template_path": "static/teams/burnley no name.jpg", "text_color": "#B1B1B1", "x": 1735, "y": 868},
    "Chelsea": {"template_path": "static/teams/CHELSEA NO NAME.jpg", "text_color": "#BDBDBD", "x": 1865, "y": 1020},
    "Crystal Palace": {"template_path": "static/teams/crystal palace no name.jpg", "text_color": "#919191", "x": 2235, "y": 868},
    "Everton": {"template_path": "static/teams/everton.jpg", "text_color": "#BBBBBB", "x": 1680, "y": 820},
    "Hull City": {"template_path": "static/teams/hull city NO NAME.jpg", "text_color": "#160E03", "x": 1680, "y": 820},
    "Liverpool": {"template_path": "static/teams/LIVERPOOL NO NAME.jpg", "text_color": "#B5B5B7", "x": 2100, "y": 950},
    "Manchester City": {"template_path": "static/teams/MANCHESTER CITY NO NAME NUMBER 10.jpg", "text_color": "#FFFFFF", "x": 1700, "y": 800},
    "Manchester United": {"template_path": "static/teams/manchester united no name on shirt.jpg", "text_color": "#A5B0AC", "x": 2150, "y": 850},
    "Newcastle": {"template_path": "static/teams/newcastle NO NAME.jpg", "text_color": "#6B1019", "x": 1730, "y": 855},
    "Leeds": {"template_path": "static/teams/NO NAME LEEDS.jpg", "text_color": "#071675", "x": 1680, "y": 820},
    "Southampton": {"template_path": "static/teams/southampton NO NAME.jpg", "text_color": "#B6B6B6", "x": 1670, "y": 830},
    "Tottenham": {"template_path": "static/teams/tottenham no name BRIGHTER.jpg", "text_color": "#3B3E51", "x": 1680, "y": 830},
    "West Ham": {"template_path": "static/teams/west ham no name.jpg", "text_color": "#B2B2B2", "x": 1680, "y": 830},
    "Wolves": {"template_path": "static/teams/wolves NO NAME.jpg", "text_color": "#000000", "x": 1735, "y": 830}
}

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    name = data.get("name", "").strip().upper()
    team = data.get("team", "")

    if not name or team not in TEAMS:
        return jsonify({"error": "Missing or invalid parameters."}), 400

    team_data = TEAMS[team]
    image_path = team_data["template_path"]
    x, y = team_data["x"], team_data["y"]
    text_color = ImageColor.getrgb(team_data["text_color"])

    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # Dynamic font size
        font_size = max(75, 130 - len(name) * 5)
        try:
            font = ImageFont.truetype(FONT_PATH, font_size)
        except:
            font = ImageFont.truetype(FALLBACK_FONT, font_size)

        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        centered_x = x - text_width // 2

        draw.text((centered_x, y), name, font=font, fill=text_color)

        # Save to buffer
        img_io = io.BytesIO()
        image.save(img_io, 'JPEG', quality=85)
        img_io.seek(0)

        return send_file(img_io, mimetype='image/jpeg')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
