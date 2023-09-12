from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, scrolledtext
from screeninfo import get_monitors
import tkinter.messagebox as messagebox

title_text = "금오산 장태호 전광판 v1.01"
font_name = "Malgun Gothic"
font_size = 30  # 초기 글자 크기 설정

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
    
def increase_font_size():
    global font_size
    font_size += 1
    label_time.config(font=(font_name, font_size))
    label_next_time.config(font=(font_name, font_size))
    label_next_next_time.config(font=(font_name, font_size))
    label.config(font=(font_name, font_size))
    font_size_entry.delete(0, tk.END)
    font_size_entry.insert(0, font_size)

def decrease_font_size():
    global font_size
    if font_size > 8:
        font_size -= 1
        label_time.config(font=(font_name, font_size))
        label_next_time.config(font=(font_name, font_size))
        label_next_next_time.config(font=(font_name, font_size))
        label.config(font=(font_name, font_size))
        font_size_entry.delete(0, tk.END)
        font_size_entry.insert(0, font_size)
            
        
# 글자 크기 업데이트 함수
def update_font_size():
    global font_size
    new_font_size_str = font_size_entry.get()
    
    try:
        new_font_size = int(new_font_size_str)
        if 8 <= new_font_size <= 300:
            font_size = new_font_size
            label_time.config(font=(font_name, font_size))
            label_next_time.config(font=(font_name, font_size))
            label_next_next_time.config(font=(font_name, font_size))
            label.config(font=(font_name, font_size))
        else:
            messagebox.showerror("오류", "글자 크기는 8에서 300 사이의 값을 입력하세요.")
    except ValueError:
        messagebox.showerror("오류", "올바른 숫자를 입력하세요.")

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
    
    # 다음 출발 남은 시간을 계산
    minute_limit_time = next_time - minute - 1
    if next_time == 0:
        minute_limit_time = 60 - minute - 1
    second_limit_time = 60 - second
    
    # hour_plus_15 = time_plus_15.hour
    # minute_plus_15 = time_plus_15.minute
    # second_plus_15 = time_plus_15.second
    # next_time_plus_15 = next_train_time(minute_plus_15)
    
    # 라벨 업데이트
    # label_time.config(text=f"현재시간: {hour:02}:{minute:02}:{second:02}")
    label_time.config(text=f"현재시간       {hour:02}:{minute:02}")
    label_next_time.config(text=f"출발시간       {(hour if next_time != 0 else hour+1):02}:{next_time:02}")
    label_next_next_time.config(text=f"다음출발       {minute_limit_time:02}분 {second_limit_time:02}초 전 입니다!")
    window1.after(1000, update_time)




# Window 1
window1 = tk.Tk()
window1.title(title_text)
window1.geometry("800x600")
window1.protocol("WM_DELETE_WINDOW", on_closing)
window1.configure(bg="black")

# 프레임 생성
frame = tk.Frame(window1, bg="black")
frame.place(relx=0.5, rely=0.5, anchor="center")  # 프레임을 윈도우의 중앙에 배치

# 라벨 위젯 생성 및 배치
label_time = tk.Label(frame, text="현재시간       ", fg="light blue", bg="black", font=(font_name, font_size))
label_next_time = tk.Label(frame, text="출발시간       ", fg="light green", bg="black", font=(font_name, font_size))
label_next_next_time = tk.Label(frame, text="다음출발       ", fg="red", bg="black", font=(font_name, font_size))
label = tk.Label(frame, text="안전을 위하여 차례차례", fg="yellow", bg="black", font=(font_name, font_size))

label_time.pack(pady=0)
label_next_time.pack(pady=0)
label_next_next_time.pack(pady=0)
label.pack(pady=0)

update_time()

# Window 2
window2 = tk.Tk()
window2.title(title_text)
window2.geometry("800x600")

# Window 2 UI
# frame_font_size 프레임
frame_font_size = tk.Frame(window2)
frame_font_size.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

font_size_label = tk.Label(frame_font_size, text="글자 크기:", font=(font_name, 16))
font_size_label.pack(side=tk.LEFT, padx=10)

font_size_entry = tk.Entry(frame_font_size, width=10, font=(font_name, 16))
font_size_entry.insert(0, font_size)
font_size_entry.pack(side=tk.LEFT)

font_size_apply_button = tk.Button(frame_font_size, text="적용", command=update_font_size, font=(font_name, 16))
font_size_apply_button.pack(side=tk.LEFT, padx=10)

# frame_buttons 프레임
frame_buttons = tk.Frame(window2)
frame_buttons.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

btn_increase_font = tk.Button(frame_buttons, text="글자 크기 +", command=increase_font_size, font=(font_name, 16))
btn_increase_font.pack(side=tk.LEFT, padx=10)

btn_decrease_font = tk.Button(frame_buttons, text="글자 크기 -", command=decrease_font_size, font=(font_name, 16))
btn_decrease_font.pack(side=tk.LEFT, padx=10)

# frame_text_update 프레임
frame_text_update = tk.Frame(window2)
frame_text_update.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

entry = scrolledtext.ScrolledText(frame_text_update, wrap=tk.NONE, height=4, width=800, font=(font_name, 16))
entry.insert("1.0", "안전을 위하여 차례차례")
entry.pack(pady=0)

horizontal_scrollbar = ttk.Scrollbar(frame_text_update, orient=tk.HORIZONTAL, command=entry.xview)
horizontal_scrollbar.pack(fill=tk.X, padx=20, pady=(0, 20))
entry.config(xscrollcommand=horizontal_scrollbar.set)

btn_update = tk.Button(frame_text_update, text="참고사항 입력완료", command=update_label, font=(font_name, 16))
btn_update.pack(side=tk.LEFT, padx=10)

btn_window2_close = tk.Button(frame_text_update, text="입력완료 후 창 내리기", command=update_label, font=(font_name, 16))
btn_window2_close.pack(side=tk.RIGHT, padx=10)

# frame_monitor 프레임
frame_monitor = tk.Frame(window2)
frame_monitor.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

monitors = [m.name for m in get_monitors()]
combo = ttk.Combobox(frame_monitor, values=monitors, font=(font_name, 16))
combo.pack(side=tk.LEFT, padx=10)

btn_fullscreen = tk.Button(frame_monitor, text="전체화면", command=set_fullscreen, font=(font_name, 16))
btn_fullscreen.pack(side=tk.LEFT, padx=10)

btn_unset_fullscreen = tk.Button(frame_monitor, text="전체화면 해제", command=unset_fullscreen, font=(font_name, 16))
btn_unset_fullscreen.pack(side=tk.LEFT, padx=10)

window1.mainloop()
window2.mainloop()
