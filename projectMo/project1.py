import datetime

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
        ] for time in times}

temp = []

class ReservationSystem:
    def __init__(self):
        self.movies = [
            Movie("범죄도시 4", ["10:00", "11:00","11:20", "16:00", "19:00", "20:15"], 19),
            Movie("귀멸의 칼날", ["11:00", "14:00","17:00", "19:07", "20:00"], 15),
            Movie("보라", ["12:00", "15:00", "16:00","18:20", "20:00","21:00", "22:00"], 12),
            Movie("영화 4", ["13:30", "14:30", "15:30","16:00","17:00", " 19:00", "20:30"], 12),
            Movie("영화 5", ["12:00", "13:30", "14:20","16:00", "19:00", "20:05"], 12)
        ]
        self.ticket_prices = {
            '성인': 18000,
            '청소년': 15000,
            '어린이': 9000
        }
        self.reservations = []

    def display_movies(self):
        global temp
        temp = [0] * len(self.movies)
        merge_sort(self.movies, 0, len(self.movies) - 1)
        print("예매 가능한 영화 목록:")
        for i, movie in enumerate(self.movies):
            print(f"{i+1}. {movie.title} (연령 제한: {movie.age_limit}세 이상)")

    def select_movie(self):
        self.display_movies()
        while True:
            try:
                choice = int(input("영화를 선택하세요 (번호 입력): ")) - 1
                if 0 <= choice < len(self.movies):
                    return self.movies[choice]
                else:
                    print("잘못된 선택입니다. 다시 입력하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    def select_date(self):
        today = datetime.datetime.today()
        print(f"오늘 날짜로 예약됩니다: {today.strftime('%Y-%m-%d')}")
        return today

    def select_time(self, movie):
        print(f"{movie.title}의 가능한 상영 시간:")
        for i, time in enumerate(movie.times):
            print(f"{i+1}. {time}")
        while True:
            try:
                choice = int(input("상영 시간을 선택하세요 (번호 입력): ")) - 1
                if 0 <= choice < len(movie.times):
                    return movie.times[choice]
                else:
                    print("잘못된 선택입니다. 다시 입력하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    def select_seat(self, movie, time, num_people):
        print(f"{movie.title}의 {time} 상영 시간의 가능한 좌석:")
        print(movie.seats[time])
        while True:
            seats = input(f"{num_people}개의 좌석을 선택하세요 (예: A1 A2 A3): ").split()
            if all(seat in movie.seats[time] for seat in seats) and len(seats) == num_people:
                for seat in seats:
                    index = movie.seats[time].index(seat)
                    movie.seats[time][index] = '■'
                return seats
            else:
                print("선택한 좌석이 유효하지 않거나, 선택한 좌석 수가 인원 수와 맞지 않습니다. 다시 선택하세요.")

    def select_num_people(self):
        print("인원을 선택하세요 (1~5명):")
        while True:
            try:
                num_people = int(input())
                if 1 <= num_people <= 5:
                    return num_people
                else:
                    print("잘못된 선택입니다. 다시 입력하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

    def check_age_restriction(self, movie, num_people):
        print(f"{movie.title}의 연령 제한은 {movie.age_limit}세 이상입니다.")
        ages = []
        for i in range(num_people):
            while True:
                try:
                    age = int(input(f"인원 {i+1}의 나이를 입력하세요: "))
                    if age >= movie.age_limit:
                        ages.append(age)
                        break
                    else:
                        print(f"해당 영화는 {movie.age_limit}세 이상만 관람할 수 있습니다. 나이가 적합하지 않습니다.")
                        return False
                except ValueError:
                    print("숫자를 입력하세요.")
        return ages

    def make_reservation(self):
        movie = self.select_movie()
        if movie:
            num_people = self.select_num_people()
            ages = self.check_age_restriction(movie, num_people)
            if ages:
                date = self.select_date()
                time = self.select_time(movie)
                seats = self.select_seat(movie, time, num_people)

                age_groups = {'성인': 0, '청소년': 0, '어린이': 0}
                for age in ages:
                    if age >= 19:
                        age_groups['성인'] += 1
                    elif age >= 13:
                        age_groups['청소년'] += 1
                    else:
                        age_groups['어린이'] += 1

                total_cost = (
                    age_groups['성인'] * self.ticket_prices['성인'] +
                    age_groups['청소년'] * self.ticket_prices['청소년'] +
                    age_groups['어린이'] * self.ticket_prices['어린이']
                )

                reservation_info = {
                    "영화": movie.title,
                    "날짜": date.date(),
                    "시간": time,
                    "좌석": seats,
                    "연령대": age_groups,
                    "총액": total_cost
                }
                self.reservations.append(reservation_info)

                age_groups_str = ", ".join([f"{k} {v}명" for k, v in age_groups.items() if v > 0])
                print(f"\n예약 정보:\n영화: {movie.title}\n날짜: {date.date()}\n시간: {time}\n좌석: {', '.join(seats)}\n연령대: {age_groups_str}\n총액: {total_cost}원")

                confirm = input("결제하시겠습니까? (yes/no): ")
                if confirm.lower() == "yes":
                    print("결제가 완료되었습니다!")
                else:
                    print("예약이 취소되었습니다.")
                    self.reservations.pop()
                print()
            else:
                print("예약이 취소되었습니다.\n")

    def view_reservations(self):
        if not self.reservations:
            print("예매 내역이 없습니다.")
        else:
            for i, reservation in enumerate(self.reservations):
                age_groups_str = ", ".join([f"{k} {v}명" for k, v in reservation['연령대'].items() if v > 0])
                print(f"{i+1}. 영화: {reservation['영화']}, 날짜: {reservation['날짜']}, 시간: {reservation['시간']}, 좌석: {', '.join(reservation['좌석'])}, 연령대: {age_groups_str}, 총액: {reservation['총액']}원")
        print()

    def run(self):
        while True:
            print("영화 예매 시스템에 오신 것을 환영합니다")
            print("1. 영화 예매")
            print("2. 예매 내역 조회")
            print("3. 종료")
            try:
                choice = int(input("번호를 선택하세요: "))
                if choice == 1:
                    self.make_reservation()
                elif choice == 2:
                    self.view_reservations()
                elif choice == 3:
                    print("프로그램을 종료합니다.")
                    self.view_reservations()
                    break
                else:
                    print("잘못된 선택입니다. 다시 선택하세요.")
            except ValueError:
                print("숫자를 입력하세요.")

if __name__ == "__main__":
    system = ReservationSystem()
    system.run()
