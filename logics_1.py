""" logics_1.py"""

def get_correct_quote(wrong_quote):
  """
  從錯誤的漲跌幅反推所有可能的正確的漲跌幅，以及其平均值

  Args:
    wrong_quote: 錯誤的漲跌幅

  Returns:
    correct_quote_range: 所有可能實際漲跌幅
    average_correct_quote: 平均實際漲跌幅
  """

  # 錯誤的漲跌幅範圍
  wrong_quote_range = range(wrong_quote + 3, wrong_quote - 4, -1)

  # 對調個位數與十位數來算出所有可能的正確的漲跌幅範圍
  correct_quote_range = []
  for i in wrong_quote_range:
   correct_quote = int(str(i)[1]+ str(i)[0])
   correct_quote_range.append(correct_quote)

  # 所有可能的正確的漲跌幅的平均值

  average_correct_quote = round(sum(correct_quote_range) / len(correct_quote_range))

  # 回傳正確的漲跌幅範圍和平均值
  return correct_quote_range, average_correct_quote

# 以輸入錯誤漲跌幅42為例
wrong_quote = 42
print("可能實際漲跌幅:", get_correct_quote(wrong_quote)[0])
print("平均實際漲跌幅:", get_correct_quote(wrong_quote)[1])