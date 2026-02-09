"""
Teaching GIF Generator: Causal Inference vs ML Prediction
Creates an animated typing battle between the two paradigms.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
WIDTH, HEIGHT = 400, 200
BG_COLOR = (30, 30, 30)  # Dark terminal background
ML_COLOR = (86, 156, 214)  # Blue for ML
CAUSAL_COLOR = (78, 201, 176)  # Teal for causal
COMMENT_COLOR = (106, 153, 85)  # Green for comments
CURSOR_COLOR = (255, 255, 255)

# The battle script (R version)
SCENES = [
    {"text": "library(caret)", "color": ML_COLOR, "action": "type"},
    {"text": "library(caret)", "color": ML_COLOR, "action": "hold"},
    {"text": "# prediction go brr", "color": COMMENT_COLOR, "action": "type", "y_offset": 30},
    {"text": "", "action": "clear"},

    {"text": "library(fixest)", "color": CAUSAL_COLOR, "action": "type"},
    {"text": "library(fixest)", "color": CAUSAL_COLOR, "action": "hold"},
    {"text": "# but is it CAUSAL?", "color": COMMENT_COLOR, "action": "type", "y_offset": 30},
    {"text": "", "action": "clear"},

    {"text": "y_hat <- predict(model, X)", "color": ML_COLOR, "action": "type"},
    {"text": "y_hat <- predict(model, X)", "color": ML_COLOR, "action": "hold"},
    {"text": "", "action": "clear"},

    {"text": "ATE <- feols(Y ~ D | FE)", "color": CAUSAL_COLOR, "action": "type"},
    {"text": "ATE <- feols(Y ~ D | FE)", "color": CAUSAL_COLOR, "action": "hold"},
    {"text": "# the real question", "color": COMMENT_COLOR, "action": "type", "y_offset": 30},
    {"text": "", "action": "clear"},
]

def get_font(size=20):
    """Try to get a monospace font, fall back to default."""
    font_paths = [
        "/System/Library/Fonts/Monaco.dfont",  # macOS
        "/System/Library/Fonts/Menlo.ttc",     # macOS
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",  # Linux
        "C:\\Windows\\Fonts\\consola.ttf",     # Windows
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

def create_frame(main_text="", main_color=ML_COLOR, comment_text="", show_cursor=True, cursor_pos=None):
    """Create a single frame of the animation."""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = get_font(22)
    small_font = get_font(16)

    # Draw prompt
    prompt = ">>> "
    draw.text((20, 80), prompt, fill=(150, 150, 150), font=font)
    prompt_width = draw.textlength(prompt, font=font)

    # Draw main text
    if main_text:
        draw.text((20 + prompt_width, 80), main_text, fill=main_color, font=font)

    # Draw cursor
    if show_cursor:
        if cursor_pos is None:
            cursor_pos = len(main_text)
        text_width = draw.textlength(main_text[:cursor_pos], font=font) if main_text else 0
        cursor_x = 20 + prompt_width + text_width
        draw.rectangle([cursor_x, 78, cursor_x + 12, 105], fill=CURSOR_COLOR)

    # Draw comment below
    if comment_text:
        draw.text((20 + prompt_width, 115), comment_text, fill=COMMENT_COLOR, font=small_font)

    return img

def create_typing_frames(text, color, comment=""):
    """Create frames for typing animation."""
    frames = []
    # Type each character
    for i in range(len(text) + 1):
        frame = create_frame(text[:i], color, comment, show_cursor=True, cursor_pos=i)
        frames.append(frame)
    return frames

def create_gif():
    """Generate the complete animation."""
    frames = []
    frame_durations = []

    current_comment = ""

    for scene in SCENES:
        action = scene["action"]

        if action == "type":
            text = scene["text"]
            color = scene.get("color", ML_COLOR)
            y_offset = scene.get("y_offset", 0)

            if y_offset > 0:  # This is a comment
                # Type the comment while keeping main text
                for i in range(len(text) + 1):
                    frame = create_frame(current_main, current_color, text[:i])
                    frames.append(frame)
                    frame_durations.append(80)
                current_comment = text
            else:
                current_main = text
                current_color = color
                current_comment = ""
                typing_frames = create_typing_frames(text, color)
                frames.extend(typing_frames)
                frame_durations.extend([80] * len(typing_frames))

        elif action == "hold":
            # Hold the current frame
            frame = create_frame(scene["text"], scene["color"], current_comment)
            for _ in range(10):  # Hold for ~800ms
                frames.append(frame)
                frame_durations.append(80)

        elif action == "clear":
            # Blink cursor on empty screen
            current_comment = ""
            for i in range(4):
                frame = create_frame("", ML_COLOR, "", show_cursor=(i % 2 == 0))
                frames.append(frame)
                frame_durations.append(150)

    # Save the gif
    output_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "teaching_code.gif")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_durations,
        loop=0
    )
    print(f"GIF saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    # Initialize variables used across scenes
    current_main = ""
    current_color = ML_COLOR

    create_gif()
    print("Done! Update teaching.md to use: image: teaching_code.gif")
