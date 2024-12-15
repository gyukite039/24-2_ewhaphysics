from datetime import datetime, timedelta

# 기본 소요 시간 (차가 막히지 않으면 1시간)
base_travel_time = 60  # 기본 소요 시간 (분)

# 사용자 입력 받기
def get_user_input():
    # 요일 입력
    day_of_week = input("오늘의 요일을 입력하세요 (예: Monday): ").capitalize()

    # 날씨 입력
    weather = input("오늘의 날씨를 입력하세요 (예: Rain, Snow, Clear): ").capitalize()

    # 행사 여부 입력
    event = input("오늘 근방에 행사가 있나요? (yes/no): ").lower()

    # 지하철 고장 여부 입력
    subway_failure = input("지하철 고장이 있나요? (yes/no): ").lower()

    return day_of_week, weather, event == "yes", subway_failure == "yes"

# 혼잡도 계산 함수
def calculate_congestion(day_of_week, weather, event, subway_failure):
    # 기본 혼잡도 (시간대에 따른 기본 값)
    congestion = 0.0

    if day_of_week == "Monday":
        congestion += 0.35  

    elif day_of_week == "Friday":
        congestion += 0.1  

    # 날씨 반영 (비와 눈의 혼잡도 처리)
    if weather == "Rain":
        congestion += 0.1 
    elif weather == "Snow":
        congestion += 0.15 

    # 행사 여부 반영
    if event:
        congestion += 0.2  

    # 지하철 고장 반영
    if subway_failure:
        congestion += 0.2 

    # 혼잡도 반환 (최대 1.0으로 제한)
    congestion = min(congestion, 1.0)
    return congestion

# 예상 도착 시간 계산 함수
def calculate_arrival_time(congestion):
    # 출발 시간 설정 (7:30 AM)
    bus_departure_time = datetime.strptime("07:30", "%H:%M")

    # 혼잡도에 따른 소요 시간 계산
    # 혼잡도가 0일 때는 60분, 1일 때는 180분 (3시간)
    additional_time = base_travel_time + (congestion * (180 - 60))  # 혼잡도에 따른 추가 시간 계산

    # 총 소요 시간 계산
    total_travel_time = additional_time

    # 예상 도착 시간 계산
    arrival_time = bus_departure_time + timedelta(minutes=total_travel_time)

    return arrival_time

# 지각 여부 확인 함수
def check_lateness(arrival_time):
    lateness_threshold = datetime.strptime("09:00", "%H:%M")  # 9시

    if arrival_time > lateness_threshold:
        return "지각입니다."
    else:
        return "시간 내 도착 가능합니다."

# 실행
def main():
    # 사용자 입력 받기
    day_of_week, weather, event, subway_failure = get_user_input()

    # 혼잡도 계산
    congestion = calculate_congestion(day_of_week, weather, event, subway_failure)

    # 예상 도착 시간 계산
    arrival_time = calculate_arrival_time(congestion)

    # 결과 출력
    print(f"\n오늘의 교통 상황:")
    print(f"요일: {day_of_week}")
    print(f"날씨: {weather}")
    print(f"행사: {'있음' if event else '없음'}")
    print(f"지하철 고장: {'있음' if subway_failure else '없음'}")
    print(f"혼잡도: {congestion*100:.0f}%")
    print(f"예상 도착 시간: {arrival_time.strftime('%H:%M')}")
    print(check_lateness(arrival_time))

if __name__ == "__main__":
    main()

