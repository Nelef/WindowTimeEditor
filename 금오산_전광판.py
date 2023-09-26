from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, scrolledtext
from screeninfo import get_monitors
import tkinter.messagebox as messagebox
import pygame

# 빌드 방법 : pyinstaller --onefile --name 금오산_케이블카_알림판_v1.4 금오산_전광판.py

departure_info = "대기시간"
title_text = "금오산 케이블카 알림판 v1.4"
font_name = "Malgun Gothic"
# font_name_bold = font.Font(family="Malgun Gothic", weight="bold")
font_size = 30  # 초기 글자 크기 설정
font_size2 = 30  # 초기 글자 크기 설정

def on_closing():
    if messagebox.askyesno("종료 확인", "프로그램을 종료하시겠습니까?"):
        window1.destroy()  # window1을 종료합니다.
        window2.destroy()  # window2를 종료합니다.

def set_fullscreen():
    window1.deiconify()  # window1 창 표시
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

# 글자 크기 업데이트 함수1
def font_size_change(size_change_value):
    global font_size
    if 8 <= (font_size + size_change_value) <= 300:
        font_size += size_change_value
        label_title_text.config(font=(font_name, int(font_size*1.2)))
        label_calendar_text.config(font=(font_name, int(font_size*0.8)))
        label_time_text.config(font=(font_name, font_size))
        label_time.config(font=(font_name, font_size))
        label_next_time_text.config(font=(font_name, font_size))
        label_next_time.config(font=(font_name, font_size))
        label_next_next_time_text.config(font=(font_name, font_size))
        label_next_next_time.config(font=(font_name, font_size))
        label_divide.config(font=(font_name, font_size-5))
        font_size_entry.delete(0, tk.END)
        font_size_entry.insert(0, font_size)
            
def update_font_size():
    global font_size
    new_font_size_str = font_size_entry.get()
    
    try:
        new_font_size = int(new_font_size_str)
        if 8 <= new_font_size <= 300:
            font_size = new_font_size
            label_title_text.config(font=(font_name, int(font_size*1.2)))
            label_calendar_text.config(font=(font_name, int(font_size*0.8)))   
            label_time_text.config(font=(font_name, font_size))
            label_time.config(font=(font_name, font_size))
            label_next_time_text.config(font=(font_name, font_size))
            label_next_time.config(font=(font_name, font_size))
            label_next_next_time_text.config(font=(font_name, font_size))
            label_next_next_time.config(font=(font_name, font_size))
            label_divide.config(font=(font_name, font_size-5))
        else:
            messagebox.showerror("오류", "글자 크기는 8에서 300 사이의 값을 입력하세요.")
    except ValueError:
        messagebox.showerror("오류", "올바른 숫자를 입력하세요.")

# 글자 크기 업데이트 함수2
def font_size_change2(size_change_value):
    global font_size2
    if 8 <= (font_size2 + size_change_value) <= 300:
        font_size2 += size_change_value
        label.config(font=(font_name, font_size2-5))  
        font_size_entry2.delete(0, tk.END)
        font_size_entry2.insert(0, font_size2)          
        
def update_font_size2():
    global font_size2
    new_font_size_str2 = font_size_entry2.get()
    
    try:
        new_font_size2 = int(new_font_size_str2)
        if 8 <= new_font_size2 <= 300:
            font_size2 = new_font_size2
            label.config(font=(font_name, font_size2-5))
        else:
            messagebox.showerror("오류", "글자 크기는 8에서 300 사이의 값을 입력하세요.")
    except ValueError:
        messagebox.showerror("오류", "올바른 숫자를 입력하세요.")



def hide_window2():
    window2.withdraw()  # window2 창 숨기기

def show_window2(event):
    window2.deiconify()  # window2 창 표시

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

    # 현재 날짜 설정
    formatted_date = current_time.strftime("(%m월 %d일)".encode('unicode-escape').decode()).encode().decode('unicode-escape')
    label_calendar_text.config(text = formatted_date)

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
    
    if minute_limit_time == 1 and second_limit_time == 1:
        mp3_file = "초인종소리.mp3"  # 재생할 MP3 파일 경로를 지정하세요
        play_mp3_once(mp3_file)
    
    # hour_plus_15 = time_plus_15.hour
    # minute_plus_15 = time_plus_15.minute
    # second_plus_15 = time_plus_15.second
    # next_time_plus_15 = next_train_time(minute_plus_15)
    
    # 라벨 업데이트
    # label_time.config(text=f"현재시간: {hour:02}:{minute:02}:{second:02}")
    label_time.config(text=f"{hour:02}시 {minute:02}분")
    label_next_time.config(text=f"{(hour if next_time != 0 else hour+1):02}시 {next_time:02}분")
    label_next_next_time.config(text=f"{minute_limit_time:02}분 {second_limit_time:02}초 전 입니다!")
    window1.after(1000, update_time)

def window1_toggle_bg_color():
    current_bg = label_next_time.cget("bg")
    if current_bg == "black":
        label_next_time.config(bg="red")
    else:
        label_next_time.config(bg="black")
    window1.after(9000, window1_toggle_bg_color)  # 10초마다 toggle_bg_color 함수 호출

def play_mp3_once(mp3_file):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()



# Window 1
window1 = tk.Tk()
window1.title(title_text)
window1.geometry("800x600")
window1.protocol("WM_DELETE_WINDOW", on_closing)
window1.configure(bg="black")
window1.bind("<Button-1>", show_window2) # frame에 클릭 이벤트를 바인딩합니다.
window1.after(2000, window1_toggle_bg_color)

# 프레임 생성
grid_frame = tk.Frame(window1, bg="black")
grid_frame.place(relx=0.5, rely=0.5, anchor="center")  # 프레임을 윈도우의 중앙에 배치

###
##### 라벨 위젯 생성 및 배치
###
# 라벨 그룹 프레임 생성
label_group_frame = tk.Frame(grid_frame, bg="black")
label_group_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))

label_title_text = tk.Label(label_group_frame, text="         출 발 시 간", fg="light green", bg="black", font=(font_name, int(font_size*1.2)))
label_title_text.grid(row=0, column=0)
label_calendar_text = tk.Label(label_group_frame, text="(다른 글자)", fg="white", bg="black", font=(font_name, int(font_size*0.8)))
label_calendar_text.grid(row=0, column=1)

label_time_text = tk.Label(grid_frame, text="현재시간", fg="light blue", bg="black", font=(font_name, font_size))
label_time_text.grid(row=1, column=0, sticky="e", padx=(0, 40))

label_time = tk.Label(grid_frame, text="00시 00분", fg="white", bg="black", font=(font_name, font_size))
label_time.grid(row=1, column=1, sticky="w")

label_next_time_text = tk.Label(grid_frame, text="출발시간", fg="light green", bg="black", font=(font_name, font_size))
label_next_time_text.grid(row=2, column=0, sticky="e", padx=(0, 40))

label_next_time = tk.Label(grid_frame, text="00시 15분", fg="white", bg="black", font=(font_name, font_size))
label_next_time.grid(row=2, column=1, sticky="w")

label_next_next_time_text = tk.Label(grid_frame, text=departure_info, fg="red", bg="black", font=(font_name, font_size))
label_next_next_time_text.grid(row=3, column=0, sticky="e", padx=(0, 40))

label_next_next_time = tk.Label(grid_frame, text="15분 00초 전 입니다!", fg="red", bg="black", font=(font_name, font_size))
label_next_next_time.grid(row=3, column=1, sticky="w")

label_divide = tk.Label(grid_frame, text="------------------------------------------------------------------------------------------------------", fg="white", bg="black", font=(font_name, font_size-5))
label_divide.grid(row=4, column=0, columnspan=2, pady=(0, 0))

label = tk.Label(grid_frame, text="♥금오산 케이블카를 이용해주셔서 감사합니다!♥\n매시 00분/15분/30분/45분 (4회 운행)\n막차 : 17시 45분", fg="yellow", bg="black", font=(font_name, font_size-5))
label.grid(row=5, column=0, columnspan=2, pady=(0, 0))

update_time()



# Window 2
window2 = tk.Tk()
window2.title(title_text)
window2.geometry("800x600")
window2.protocol("WM_DELETE_WINDOW", on_closing)

# Window 2 UI
# frame_font_size 프레임
frame_font_size = tk.Frame(window2)
frame_font_size.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

font_size_label = tk.Label(frame_font_size, text="시간 글자 크기:", font=(font_name, 16))
font_size_label.pack(side=tk.LEFT, padx=10)

btn_decrease_font = tk.Button(frame_font_size, text="-5", width=3, command=lambda: font_size_change(-5), font=(font_name, 16))
btn_decrease_font.pack(side=tk.LEFT, padx=(5, 0))
btn_decrease_font = tk.Button(frame_font_size, text="-1", width=3, command=lambda: font_size_change(-1), font=(font_name, 16))
btn_decrease_font.pack(side=tk.LEFT, padx=(5, 0))
btn_increase_font = tk.Button(frame_font_size, text="+1", width=3, command=lambda: font_size_change(+1), font=(font_name, 16))
btn_increase_font.pack(side=tk.LEFT, padx=(5, 0))
btn_increase_font = tk.Button(frame_font_size, text="+5", width=3, command=lambda: font_size_change(+5), font=(font_name, 16))
btn_increase_font.pack(side=tk.LEFT, padx=5)

font_size_entry = tk.Entry(frame_font_size, width=10, font=(font_name, 16))
font_size_entry.insert(0, font_size)
font_size_entry.pack(side=tk.LEFT)

font_size_apply_button = tk.Button(frame_font_size, text="적용", command=update_font_size, font=(font_name, 16))
font_size_apply_button.pack(side=tk.LEFT, padx=10)

# frame_text_update 프레임
frame_text_update = tk.Frame(window2)
frame_text_update.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

entry = scrolledtext.ScrolledText(frame_text_update, wrap=tk.NONE, height=4, width=800, font=(font_name, 16))
entry.insert("1.0", "♥금오산 케이블카를 이용해주셔서 감사합니다!♥\n매시 00분/15분/30분/45분 (4회 운행)\n막차 : 17시 45분")
entry.pack(pady=0)

horizontal_scrollbar = ttk.Scrollbar(frame_text_update, orient=tk.HORIZONTAL, command=entry.xview)
horizontal_scrollbar.pack(fill=tk.X, padx=20, pady=(0, 20))
entry.config(xscrollcommand=horizontal_scrollbar.set)

btn_update = tk.Button(frame_text_update, text="참고사항 입력완료", command=update_label, font=(font_name, 16))
btn_update.pack(side=tk.LEFT, padx=10)

# frame_font_size2 프레임
frame_font_size2 = tk.Frame(window2)
frame_font_size2.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

font_size_label2 = tk.Label(frame_font_size2, text="텍스트 글자 크기:", font=(font_name, 16))
font_size_label2.pack(side=tk.LEFT, padx=10)

btn_decrease_font2 = tk.Button(frame_font_size2, text="-5", width=3, command=lambda: font_size_change2(-5), font=(font_name, 16))
btn_decrease_font2.pack(side=tk.LEFT, padx=(5, 0))
btn_decrease_font2 = tk.Button(frame_font_size2, text="-1", width=3, command=lambda: font_size_change2(-1), font=(font_name, 16))
btn_decrease_font2.pack(side=tk.LEFT, padx=(5, 0))
btn_increase_font2 = tk.Button(frame_font_size2, text="+1", width=3, command=lambda: font_size_change2(+1), font=(font_name, 16))
btn_increase_font2.pack(side=tk.LEFT, padx=(5, 0))
btn_increase_font2 = tk.Button(frame_font_size2, text="+5", width=3, command=lambda: font_size_change2(+5), font=(font_name, 16))
btn_increase_font2.pack(side=tk.LEFT, padx=5)

font_size_entry2 = tk.Entry(frame_font_size2, width=10, font=(font_name, 16))
font_size_entry2.insert(0, font_size2)
font_size_entry2.pack(side=tk.LEFT)

font_size_apply_button2 = tk.Button(frame_font_size2, text="적용", command=update_font_size2, font=(font_name, 16))
font_size_apply_button2.pack(side=tk.LEFT, padx=10)

# frame_monitor 프레임
frame_monitor = tk.Frame(window2)
frame_monitor.pack(side=tk.TOP, padx=10, pady=50, fill=tk.X)

monitors = [m.name for m in get_monitors()]
combo = ttk.Combobox(frame_monitor, values=monitors, font=(font_name, 16))
combo.set(monitors[0]) # 첫 번째 항목을 선택하도록 초기 설정
combo.pack(side=tk.LEFT, padx=10)

btn_fullscreen = tk.Button(frame_monitor, text="전체화면", command=set_fullscreen, font=(font_name, 16))
btn_fullscreen.pack(side=tk.LEFT, padx=10)

btn_unset_fullscreen = tk.Button(frame_monitor, text="전체화면 해제", command=unset_fullscreen, font=(font_name, 16))
btn_unset_fullscreen.pack(side=tk.LEFT, padx=10)

btn_window2_close = tk.Button(window2, text="창 숨기기", command=hide_window2, font=(font_name, 16))
btn_window2_close.pack(side=tk.TOP, pady=0)

window2.mainloop()
window1.mainloop()
