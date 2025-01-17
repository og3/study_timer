import datetime
import time
from win10toast import ToastNotifier

TOAST_DURATION_SEC = 5
NOTIFICATION_INTERVAL_SEC = 300

# 現在の時限を取得する（文字列で比較する）
def get_current_period(timetable, current_time):
    for i, (start, end) in enumerate(timetable, 1):
        if start <= current_time <= end:
            return i
    return "休憩中"

# 終了までの残り時間を分単位で取得する（datetimeオブジェクトで計算する）
def get_remaining_minutes(start, end):
    start_time = datetime.datetime.strptime(start, "%H:%M")
    end_time = datetime.datetime.strptime(end, "%H:%M")
    remaining_time = end_time - start_time
    return remaining_time.seconds // 60

def show_toast(title, message, duration_sec=TOAST_DURATION_SEC):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=duration_sec)

def main():
    timetable = [
        ("09:30", "10:15"),
        ("10:25", "11:10"),
        ("11:20", "12:05"),
        ("12:55", "13:40"),
        ("13:50", "14:35"),
        ("14:45", "15:30"),
    ]

    end_time = "15:30"
    
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        remaining_to_end = get_remaining_minutes(current_time, end_time)
        if current_time >= end_time:
            show_toast("下校時間です！", "お疲れさまでした。(スクリプトを終了します)")
            break

        period = get_current_period(timetable, current_time)

        if period != "休憩中":
            end = timetable[period - 1][1]
            remaining = get_remaining_minutes(current_time, end)
            show_toast(f"現在{period}時限目です", f"授業はあと{remaining}分で終わります。\n下校まであと{remaining_to_end}分です。")
        else:
           show_toast("休憩中", f"下校まであと{remaining_to_end}分です。")

        # 5分間隔で実行すための待機
        time.sleep(NOTIFICATION_INTERVAL_SEC)

# Pythonのスクリプトが直接実行された場合にのみ実行する
if __name__ == "__main__":
    main()
