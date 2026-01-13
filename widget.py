import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import json
import os

from widget_styles import (
    BG, CARD, TEXT, ACCENT, SUBTLE, MSG_BG,
    WINDOW_WIDTH, WINDOW_HEIGHT, CARD_WIDTH, CARD_HEIGHT,
    CORNER_RADIUS,
    MASCOT_MAX_WIDTH, MASCOT_MAX_HEIGHT, MASCOT_PADY,
    FONT_STOCK, FONT_PRICE, FONT_MSG, FONT_TIME,
    PRICE_PADY, MSG_PADY, MSG_WRAP, MSG_PADX, TIME_PADY
)

# Use absolute path based on script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIDGET_FILE = os.path.join(SCRIPT_DIR, "widget_data.json")
MASCOT_FILE = os.path.join(SCRIPT_DIR, "mascot.png")


def create_rounded_rectangle_image(width, height, radius, color):
    """Create a rounded rectangle image for the card background."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [(0, 0), (width - 1, height - 1)],
        radius=radius,
        fill=color
    )
    return img


# Window setup
root = tk.Tk()
root.title("Market Buddy")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg=BG)
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-transparent", True)

# Draggable widget - track offset from click position
drag_offset_x = 0
drag_offset_y = 0

def start_drag(event):
    global drag_offset_x, drag_offset_y
    drag_offset_x = event.x
    drag_offset_y = event.y

def drag(event):
    x = event.x_root - drag_offset_x
    y = event.y_root - drag_offset_y
    root.geometry(f"+{x}+{y}")

root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", drag)

# Rounded card background using Canvas
canvas = tk.Canvas(
    root,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    bg=BG,
    highlightthickness=0
)
canvas.pack(fill="both", expand=True)

# Create rounded rectangle background
card_x = (WINDOW_WIDTH - CARD_WIDTH) // 2
card_y = (WINDOW_HEIGHT - CARD_HEIGHT) // 2

rounded_bg = create_rounded_rectangle_image(CARD_WIDTH, CARD_HEIGHT, CORNER_RADIUS, CARD)
rounded_bg_tk = ImageTk.PhotoImage(rounded_bg)
canvas.create_image(card_x, card_y, anchor="nw", image=rounded_bg_tk)
canvas.rounded_bg_tk = rounded_bg_tk  # Keep reference

# Card frame (transparent, placed over the rounded background)
card = tk.Frame(root, bg=CARD, bd=0, highlightthickness=0)
card.place(x=card_x + 10, y=card_y + 10, width=CARD_WIDTH - 20, height=CARD_HEIGHT - 20)

# Mascot (resized to fit)
if os.path.exists(MASCOT_FILE):
    img = Image.open(MASCOT_FILE)
    img.thumbnail((MASCOT_MAX_WIDTH, MASCOT_MAX_HEIGHT), Image.Resampling.LANCZOS)
    mascot_img = ImageTk.PhotoImage(img)
    mascot = tk.Label(card, image=mascot_img, bg=CARD)
    mascot.image = mascot_img
    mascot.pack(pady=MASCOT_PADY)
else:
    print(f"[DEBUG] Mascot not found at: {MASCOT_FILE}")

# Stock name
stock_label = tk.Label(
    card,
    text="—",
    font=FONT_STOCK,
    bg=CARD,
    fg=TEXT
)
stock_label.pack()

# Price
price_label = tk.Label(
    card,
    text="₹ —",
    font=FONT_PRICE,
    bg=CARD,
    fg=ACCENT
)
price_label.pack(pady=PRICE_PADY)

# Message bubble
msg_label = tk.Label(
    card,
    text="waiting for market magic...",
    wraplength=MSG_WRAP,
    justify="center",
    font=FONT_MSG,
    bg=MSG_BG,
    fg=TEXT,
    padx=MSG_PADX,
    pady=MSG_PADX
)
msg_label.pack(pady=MSG_PADY)

# Time
time_label = tk.Label(
    card,
    text="",
    font=FONT_TIME,
    bg=CARD,
    fg=SUBTLE
)
time_label.pack(pady=TIME_PADY)

# Update loop
def update_widget():
    if os.path.exists(WIDGET_FILE):
        try:
            with open(WIDGET_FILE) as f:
                data = json.load(f)

            stock_label.config(text=data.get("stock", "—"))
            price_label.config(text=f"₹ {data.get('price', '—')}")
            msg_label.config(text=data.get("message", "—"))
            time_label.config(text=f"updated {data.get('time', '')}")

        except Exception as e:
            print(f"[DEBUG] Error reading widget data: {e}")
    else:
        print(f"[DEBUG] Widget file not found: {WIDGET_FILE}")

    root.after(3000, update_widget)

update_widget()
root.mainloop()
