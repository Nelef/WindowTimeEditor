from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors
import tkinter.messagebox as messagebox
from tkinter import scrolledtext

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
    label.config(text=entry.get("1.0", "end-1c"))
    
##
## 열차 시각 계산
##
def next_train_time(current_minutes):
    # 열차의 출발 시간 배열
    train_times = [0, 15, 30, 45]
    for t in train_times:
        if current_minutes < t:
            return t
    return 0  # 다음 시간의 0분에 출발

def next_next_train_time(next_time_minutes):
    # 다음 열차의 출발 시간을 반환
    if next_time_minutes == 45:
        return 0
    return next_time_minutes + 15

def update_time():
    current_time = datetime.now()
    time_plus_15 = current_time + timedelta(minutes=15)

    # 다음 출발 시간 계산
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second
    next_time = next_train_time(minute)
    
    # 그 다음 출발 시간을 계산
    hour_plus_15 = time_plus_15.hour
    minute_plus_15 = time_plus_15.minute
    second_plus_15 = time_plus_15.second
    next_time_plus_15 = next_train_time(minute_plus_15)
    
    # 라벨 업데이트
    # label_time.config(text=f"현재시간: {hour:02}:{minute:02}:{second:02}")
    label_time.config(text=f"현재시간       {hour:02}:{minute:02}")
    label_next_time.config(text=f"출발시간       {(hour if next_time != 0 else hour+1):02}:{next_time:02}")
    label_next_next_time.config(text=f"다음출발       {(hour_plus_15 if next_time_plus_15 != 0 else hour_plus_15+1):02}:{next_time_plus_15:02}")
    window1.after(1000, update_time)




# Window 1
window1 = tk.Tk()
window1.title("window 1th")
window1.geometry("800x600")
window1.protocol("WM_DELETE_WINDOW", on_closing)
window1.configure(bg="black")

# 프레임 생성
frame = tk.Frame(window1, bg="black")
frame.place(relx=0.5, rely=0.5, anchor="center")  # 프레임을 윈도우의 중앙에 배치

# 라벨 위젯 생성 및 배치
label_time = tk.Label(frame, text="현재시간       ", fg="light blue", bg="black", font=("Helvetica", 16))
label_next_time = tk.Label(frame, text="출발시간       ", fg="light green", bg="black", font=("Helvetica", 16))
label_next_next_time = tk.Label(frame, text="다음출발       ", fg="yellow", bg="black", font=("Helvetica", 16))
label = tk.Label(frame, text="안전을 위하여 차례차례", fg="red", bg="black", font=("Helvetica", 16))

label_time.pack(pady=0)
label_next_time.pack(pady=0)
label_next_next_time.pack(pady=0)
label.pack(pady=0)

update_time()

# Window 2
window2 = tk.Tk()
window2.title("window 2th")
window2.geometry("800x600")
window2.protocol("WM_DELETE_WINDOW", on_closing)

# 스크롤 가능한 Text 위젯으로 변경하고 기본 텍스트를 설정합니다.
entry = scrolledtext.ScrolledText(window2, wrap=tk.WORD, height=3, width=40, font=("Helvetica", 16))
entry.insert("1.0", "안전을 위하여 차례차례")  # 기본 텍스트 설정
entry.pack(pady=20)

btn_update = tk.Button(window2, text="확인", command=update_label, font=("Helvetica", 16))
btn_update.pack(pady=10)

monitors = [m.name for m in get_monitors()]
combo = ttk.Combobox(window2, values=monitors, font=("Helvetica", 16))
combo.pack(pady=20)

btn_fullscreen = tk.Button(window2, text="전체화면", command=set_fullscreen, font=("Helvetica", 16))
btn_fullscreen.pack(pady=10)

btn_unset_fullscreen = tk.Button(window2, text="전체화면 해제", command=unset_fullscreen, font=("Helvetica", 16))
btn_unset_fullscreen.pack(pady=10)

window1.mainloop()
window2.mainloop()
