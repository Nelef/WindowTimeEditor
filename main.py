import datetime
import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors
import tkinter.messagebox as messagebox

def on_closing():
    if messagebox.askyesno("종료 확인", "프로그램을 종료하시겠습니까?"):
        window1.destroy()  # window1을 종료합니다.
        window2.destroy()  # window2를 종료합니다.
    
def set_fullscreen():
    selected_monitor = combo.get()
    for m in get_monitors():
        if m.name == selected_monitor:
            window1.geometry(f"{m.width}x{m.height}+{m.x}+{m.y}")
            window1.overrideredirect(True)
            break

def unset_fullscreen():
    window1.overrideredirect(False)
    window1.geometry("800x600")

def update_label():
    label.config(text=entry.get())

# Window 1
window1 = tk.Tk()
window1.title("window 1th")
window1.geometry("800x600")
window1.protocol("WM_DELETE_WINDOW", on_closing)

monitors = [m.name for m in get_monitors()]
combo = ttk.Combobox(window1, values=monitors)
combo.pack(pady=20)

btn_fullscreen = tk.Button(window1, text="전체화면", command=set_fullscreen)
btn_fullscreen.pack(pady=10)

btn_unset_fullscreen = tk.Button(window1, text="전체화면 해제", command=unset_fullscreen)
btn_unset_fullscreen.pack(pady=10)

label_time = tk.Label(window1, text="")
label_time.pack(pady=20)
def update_time():
    current_time = datetime.datetime.now().strftime('%H:%M:%S')  # 이 부분을 수정합니다.
    label_time.config(text=current_time)
    window1.after(1000, update_time)
update_time()

label = tk.Label(window1, text="test")
label.pack(pady=20)

# Window 2
window2 = tk.Tk()
window2.title("window 2th")
window2.geometry("800x600")
window2.protocol("WM_DELETE_WINDOW", on_closing)

entry = tk.Entry(window2)
entry.pack(pady=20)

btn_update = tk.Button(window2, text="확인", command=update_label)
btn_update.pack(pady=10)

window1.mainloop()
window2.mainloop()
