import datetime
import time
import sys

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

def main():
    timetable = [
        ("09:30", "10:15"),
        ("10:25", "11:10"),
        ("11:20", "12:05"),
        ("12:55", "13:40"),
        ("13:50", "14:35"),
        ("14:45", "15:30"),
    ]
    # 下校時刻だけを文字列で設定していてdatetimeオブジェクトで比較できないので冗長を許容
    end_time = datetime.datetime.strptime("15:30", "%H:%M").strftime("%H:%M")

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time >= end_time:
            print("下校時間です！お疲れさまでした。(スクリプトを終了します)")
            # スクリプトを終了
            sys.exit()
            break

        period = get_current_period(timetable, current_time)

        if period != "休憩中":
            end = timetable[period - 1][1]
            remaining = get_remaining_minutes(current_time, end)
            print(f"現在{period}時限目です。授業はあと{remaining}分で終わります。")
        else:
            print("休憩中です")

        # 下校までの残り時間
        remaining_to_end = get_remaining_minutes(current_time, end_time)
        print(f"下校まであと{remaining_to_end}分です。")

        # 5分間隔で実行すための待機
        time.sleep(300)

# Pythonのスクリプトが直接実行された場合にのみ実行する
if __name__ == "__main__":
    main()
