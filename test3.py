import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re
import json
import os

class Movie:
    def __init__(self, title, times, age_limit):
        self.title = title
        self.times = times
        self.age_limit = age_limit
        self.seats = {time: [
            'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
            'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 
            'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 
            'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 
            'E1', 'E2', 'E3', 'E4', 'E5', 'E6',
            'F1', 'F2', 'F3', 'F4', 'F5', 'F6'
        ] for time in times}
    
    def to_dict(self):
        return {
            'title': self.title,
            'times': self.times,
            'age_limit': self.age_limit,
            'seats': self.seats
        }

    @classmethod
    def from_dict(cls, data):
        movie = cls(data['title'], data['times'], data['age_limit'])
        movie.seats = data['seats']
        return movie

class ReservationSystem:
    def __init__(self, root):
        self.root = root
        self.movies = [
            Movie("범죄도시 4", ["10:00", "11:00", "11:20", "16:00", "19:00", "20:15"], 19),
            Movie("귀멸의 칼날", ["11:00", "14:00", "17:00", "19:07", "20:00"], 15),
            Movie("보라", ["12:00", "15:00", "16:00", "18:20", "20:00", "21:00", "22:00"], 12),
            Movie("영화 4", ["13:30", "14:30", "15:30", "16:00", "17:00", "19:00", "20:30"], 12),
            Movie("영화 5", ["12:00", "13:30", "14:20", "16:00", "19:00", "20:05"], 12)
        ]
        self.ticket_prices = {
            '성인': 18000,
            '청소년': 15000,
            '어린이': 9000
        }
        self.reservations = {}
        self.current_phone_number = ""
        
        self.load_data()

        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.login_frame()
    
    def load_data(self):
        if os.path.exists('reservations.json'):
            with open('reservations.json', 'r') as file:
                self.reservations = json.load(file)
    
    def save_data(self):
        with open('reservations.json', 'w') as file:
            json.dump(self.reservations, file)
    
    def login_frame(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="영화 예매 시스템에 오신 것을 환영합니다").grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.main_frame, text="전화번호를 입력하세요 (예: 010-1234-5678):").grid(row=1, column=0, sticky='e')
        self.phone_entry = ttk.Entry(self.main_frame)
        self.phone_entry.grid(row=1, column=1)
        
        ttk.Label(self.main_frame, text="비밀번호를 입력하세요:").grid(row=2, column=0, sticky='e')
        self.password_entry = ttk.Entry(self.main_frame, show="*")
        self.password_entry.grid(row=2, column=1)
        
        login_button = ttk.Button(self.main_frame, text="로그인", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        register_button = ttk.Button(self.main_frame, text="회원가입", command=self.register_frame)
        register_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def register_frame(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="회원가입").grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.main_frame, text="전화번호를 입력하세요 (예: 010-1234-5678):").grid(row=1, column=0, sticky='e')
        self.register_phone_entry = ttk.Entry(self.main_frame)
        self.register_phone_entry.grid(row=1, column=1)
        
        ttk.Label(self.main_frame, text="비밀번호를 입력하세요:").grid(row=2, column=0, sticky='e')
        self.register_password_entry = ttk.Entry(self.main_frame, show="*")
        self.register_password_entry.grid(row=2, column=1)
        
        ttk.Label(self.main_frame, text="비밀번호를 다시 입력하세요:").grid(row=3, column=0, sticky='e')
        self.register_confirm_password_entry = ttk.Entry(self.main_frame, show="*")
        self.register_confirm_password_entry.grid(row=3, column=1)
        
        register_button = ttk.Button(self.main_frame, text="가입", command=self.register)
        register_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def register(self):
        phone_number = self.register_phone_entry.get()
        password = self.register_password_entry.get()
        confirm_password = self.register_confirm_password_entry.get()
        
        if not re.match(r"010-\d{4}-\d{4}$", phone_number):
            messagebox.showerror("오류", "전화번호 형식이 올바르지 않습니다. 다시 입력하세요.")
            return
        
        if password != confirm_password:
            messagebox.showerror("오류", "비밀번호가 일치하지 않습니다. 다시 입력하세요.")
            return
        
        if phone_number in self.reservations:
            messagebox.showerror("오류", "이미 가입된 전화번호입니다.")
            return
        
        self.reservations[phone_number] = {'password': password, 'reservations': []}
        self.save_data()
        messagebox.showinfo("가입 완료", "회원가입이 완료되었습니다.")
        self.login_frame()
    
    def login(self):
        phone_number = self.phone_entry.get()
        password = self.password_entry.get()
        
        if re.match(r"010-\d{4}-\d{4}$", phone_number):
            if phone_number in self.reservations and self.reservations[phone_number]['password'] == password:
                self.current_phone_number = phone_number
                self.main_menu()
            else:
                messagebox.showerror("오류", "전화번호 또는 비밀번호가 올바르지 않습니다.")
        else:
            messagebox.showerror("오류", "전화번호 형식이 올바르지 않습니다. 다시 입력하세요.")
    
    def main_menu(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text=f"{self.current_phone_number}으로 로그인되었습니다.").grid(row=0, column=0, columnspan=2, pady=10)
        
        reserve_button = ttk.Button(self.main_frame, text="1. 영화 예매", command=self.make_reservation)
        reserve_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        view_button = ttk.Button(self.main_frame, text="2. 예매 내역 조회", command=self.view_reservations)
        view_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        logout_button = ttk.Button(self.main_frame, text="3. 로그아웃", command=self.logout)
        logout_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    def logout(self):
        self.current_phone_number = ""
        self.login_frame()

    def make_reservation(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text="영화를 선택하세요:").grid(row=0, column=0, columnspan=2, pady=10)
        
        self.movie_listbox = tk.Listbox(self.main_frame)
        for movie in self.movies:
            self.movie_listbox.insert(tk.END, f"{movie.title} (연령 제한: {movie.age_limit}세 이상)")
        self.movie_listbox.grid(row=1, column=0, columnspan=2, pady=10)
        
        select_button = ttk.Button(self.main_frame, text="선택", command=self.select_movie)
        select_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    def select_movie(self):
        try:
            index = self.movie_listbox.curselection()[0]
            self.selected_movie = self.movies[index]
            self.select_time()
        except IndexError:
            messagebox.showerror("오류", "영화를 선택하세요.")
    
    def select_time(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text=f"{self.selected_movie.title}의 상영 시간을 선택하세요:").grid(row=0, column=0, columnspan=2, pady=10)
        
        self.time_listbox = tk.Listbox(self.main_frame)
        for time in self.selected_movie.times:
            self.time_listbox.insert(tk.END, time)
        self.time_listbox.grid(row=1, column=0, columnspan=2, pady=10)
        
        select_button = ttk.Button(self.main_frame, text="선택", command=self.select_seat)
        select_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    def select_seat(self):
        try:
            index = self.time_listbox.curselection()[0]
            self.selected_time = self.selected_movie.times[index]
            self.clear_frame()
            ttk.Label(self.main_frame, text=f"{self.selected_movie.title} ({self.selected_time})의 좌석을 선택하세요:").grid(row=0, column=0, columnspan=2, pady=10)
            
            self.seat_listbox = tk.Listbox(self.main_frame)
            for seat in self.selected_movie.seats[self.selected_time]:
                self.seat_listbox.insert(tk.END, seat)
            self.seat_listbox.grid(row=1, column=0, columnspan=2, pady=10)
            
            select_button = ttk.Button(self.main_frame, text="선택", command=self.confirm_reservation)
            select_button.grid(row=2, column=0, columnspan=2, pady=10)
        except IndexError:
            messagebox.showerror("오류", "상영 시간을 선택하세요.")
    
    def confirm_reservation(self):
        try:
            index = self.seat_listbox.curselection()[0]
            self.selected_seat = self.seat_listbox.get(index)
            self.clear_frame()
            
            self.selected_movie.seats[self.selected_time].remove(self.selected_seat)
            
            reservation = {
                'movie': self.selected_movie.title,
                'time': self.selected_time,
                'seat': self.selected_seat
            }
            
            self.reservations[self.current_phone_number]['reservations'].append(reservation)
            self.save_data()
            
            ttk.Label(self.main_frame, text="예약이 완료되었습니다!").grid(row=0, column=0, columnspan=2, pady=10)
            main_menu_button = ttk.Button(self.main_frame, text="메인 메뉴로", command=self.main_menu)
            main_menu_button.grid(row=1, column=0, columnspan=2, pady=10)
        except IndexError:
            messagebox.showerror("오류", "좌석을 선택하세요.")
    
    def view_reservations(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text=f"{self.current_phone_number}의 예매 내역:").grid(row=0, column=0, columnspan=2, pady=10)
        
        reservation_listbox = tk.Listbox(self.main_frame)
        for reservation in self.reservations[self.current_phone_number]['reservations']:
            reservation_listbox.insert(tk.END, f"{reservation['movie']} - {reservation['time']} - {reservation['seat']}")
        reservation_listbox.grid(row=1, column=0, columnspan=2, pady=10)
        
        back_button = ttk.Button(self.main_frame, text="메인 메뉴로", command=self.main_menu)
        back_button.grid(row=2, column=0, columnspan=2, pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("영화 예매 시스템")
    app = ReservationSystem(root)
    root.mainloop()
