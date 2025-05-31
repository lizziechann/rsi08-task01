import tkinter as tk
from PIL import Image, ImageTk
import time
import os

folder_path = "C:/Users/wangy/OneDrive/Desktop/rsi08/python project"
background_name = "imag1.png"
durations = [1.5, 2]
gap_between = 0.5
max_trials = 4

# load images
image_files = [f for f in os.listdir(folder_path) if f.endswith((".jpg", ".png"))]
image_paths = [os.path.join(folder_path, f) for f in image_files]
background_path = next(p for p in image_paths if background_name in p)
overlay_paths = sorted([p for p in image_paths if background_name not in p])

single_trial_overlays = []
current_time = 0.5
for path, dur in zip(overlay_paths, durations):
    single_trial_overlays.append({
        "path": path,
        "start": current_time,
        "duration": dur
    })
    current_time += dur + gap_between

total_duration = current_time - gap_between
all_trials = [single_trial_overlays.copy() for _ in range(max_trials)]

reaction_times = []
trial_index = 0
imag4_start_time = None
imag4_box = None
start_time = None

root = tk.Tk()
root.title("Reaction Time Task")
bg_img = Image.open(background_path).convert("RGBA")
bg_w, bg_h = bg_img.size
tk_bg = ImageTk.PhotoImage(bg_img)

canvas = tk.Canvas(root, width=bg_w, height=bg_h)
canvas.pack()
img_id = canvas.create_image(0, 0, anchor="nw", image=tk_bg)

# clicking to end trial
def on_click(event):
    global imag4_start_time, trial_index
    if imag4_start_time and imag4_box:
        x1, y1, x2, y2 = imag4_box
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            rt = time.time() - imag4_start_time
            reaction_times.append(rt)
            print(f"Trial {trial_index + 1} Reaction time: {rt:.3f} seconds")
            next_trial()

canvas.bind("<Button-1>", on_click)

def next_trial():
    global trial_index, imag4_start_time, imag4_box, start_time
    trial_index += 1
    if trial_index >= max_trials:
        avg = sum(reaction_times) / len(reaction_times)
        print(f"\nAverage Reaction Time: {avg:.3f} seconds")
        root.destroy()
    else:
        imag4_start_time = None
        imag4_box = None
        start_time = time.time()
        update_frame()

def update_frame():
    global imag4_start_time, imag4_box, start_time
    if start_time is None:
        start_time = time.time()
    elapsed = time.time() - start_time
    trial = all_trials[trial_index]

    frame = bg_img.copy()
    for overlay in trial:
        if overlay["start"] <= elapsed <= overlay["start"] + overlay["duration"]:
            ov_img = Image.open(overlay["path"]).convert("RGBA")
            ow, oh = ov_img.size
            x = (bg_w - ow) // 2
            y = (bg_h - oh) // 2

            if "imag2" in overlay["path"]:
                scale = min((bg_w * 0.4) / ow, (bg_h * 0.4) / oh)
                ov_img = ov_img.resize((int(ow * scale), int(oh * scale)), Image.LANCZOS)
                ow, oh = ov_img.size
                x = (bg_w - ow) // 2
                y = (bg_h - oh) // 2

            if "imag4.png" in overlay["path"]:
                if imag4_start_time is None:
                    imag4_start_time = time.time()
                    imag4_box = (x, y, x + ow, y + oh)

            frame.paste(ov_img, (x, y), ov_img)

    # max timing for no click
    if imag4_start_time:
        imag4_overlay = next((o for o in trial if "imag4.png" in o["path"]), None)
        if imag4_overlay:
            max_rt = imag4_overlay["duration"]
            if time.time() - imag4_start_time > max_rt and len(reaction_times) == trial_index:
                reaction_times.append(max_rt)
                print(f"Trial {trial_index + 1} Reaction time (no click): {max_rt:.3f} seconds")
                next_trial()
                return

    tk_frame = ImageTk.PhotoImage(frame)
    canvas.itemconfig(img_id, image=tk_frame)
    canvas.image = tk_frame

    root.after(50, update_frame)

update_frame()
root.mainloop()
