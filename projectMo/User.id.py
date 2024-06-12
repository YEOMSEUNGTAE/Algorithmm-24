import tkinter as tk
from tkinter import messagebox

# 임시 데이터베이스로 전화번호와 비밀번호를 저장
users = {}

# 회원가입 함수
def register():
    def submit_registration():
        phone = phone_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        
        if password != confirm_password:
            messagebox.showerror("오류", "비밀번호를 다시 입력해 주세요.")
            return
        
        if phone in users:
            messagebox.showerror("오류", "이 전화번호는 이미 가입되어 있습니다.")
        else:
            users[phone] = password
            messagebox.showinfo("Success", "회원가입이 완료되었습니다!")
            register_window.destroy()

    register_window = tk.Toplevel(root)
    register_window.title("회원가입")

    tk.Label(register_window, text="전화번호").pack()
    phone_entry = tk.Entry(register_window)
    phone_entry.pack()

    tk.Label(register_window, text="비밀번호").pack()
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack()
    
    tk.Label(register_window, text="비밀번호 재입력").pack()
    confirm_password_entry = tk.Entry(register_window, show="*")
    confirm_password_entry.pack()

    tk.Button(register_window, text="가입", command=submit_registration).pack()

# 로그인 함수
def login():
    phone = phone_entry.get()
    password = password_entry.get()
    
    if phone in users and users[phone] == password:
        messagebox.showinfo("성공", "로그인이 완료되었습니다!")
    else:
        messagebox.showerror("오류", "전화번호()와 비밀번호가 맞지 않습니다.")

# Tkinter GUI 초기 설정
root = tk.Tk()
root.title("로그인")

# 전화번호 레이블과 입력창
tk.Label(root, text="전화번호").pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

# 비밀번호 레이블과 입력창
tk.Label(root, text="비밀번호").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# 로그인 버튼
tk.Button(root, text="로그인", command=login).pack()

# 회원가입 버튼
tk.Button(root, text="회원가입", command=register).pack()

# GUI 루프 시작
root.mainloop()