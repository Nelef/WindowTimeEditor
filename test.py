import tkinter as tk

root = tk.Tk()
root.title("2x3 그리드")

# 윈도우 크기 설정
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 그리드 프레임 생성
grid_frame = tk.Frame(root)
grid_frame.place(relx=0.5, rely=0.5, anchor="center")

def create_label(text, row, column):
    label = tk.Label(grid_frame, text=text, padx=20, pady=10)
    label.grid(row=row, column=column)

create_label("(0, 0)", 0, 0)
create_label("(0, 1)", 0, 1)
create_label("(0, 2)", 0, 2)
create_label("(1, 0)", 1, 0)
create_label("(1, 1)1111", 1, 1)
create_label("(1, 2)", 1, 2)

root.mainloop()
