# time_strings = [f"16:{minute:02d}" for minute in range(1, 60)]
# print(time_strings)
#
#
# time_strings = [str(i) for i in range(61010, 62001, 10)]
# print(time_strings)

# 滚动收益率
# 每日收益复投
start_money = 52000
daily_rate = 0.2 / 365
days = 365
# 每日复投
for i in range(days):
    start_money = start_money * (1 + daily_rate)
    print(f"第{i+1}天, 收益: {start_money}")