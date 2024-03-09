""" logics_2.py"""
import re

def count_letters(text):
  """
  計算字串中每個字母出現次數(字母大小寫視為不同)

  Args:
    text: 輸入需要計算的字串

  Returns:
    sorted_letter_counts: 每個字母的出現次數
  """
  # 去除空格與標點符號
  text = re.sub(r"[^\w]", "", text)

  # 統計字母出現次數
  letter_counts = {}
  for letter in text:
   if letter not in letter_counts:
    # Key的初始值為0, 避免Key Error
    letter_counts[letter] = 0
   letter_counts[letter] += 1
  # 由大到小排序出現次數
  # 如出現次數一樣, 按照字母標順序排序
  sorted_letter_counts = dict(sorted(letter_counts.items(), key=lambda x:(-x[1], x[0])))

  # 回傳字母出現次數
  return sorted_letter_counts

# 輸入"Hello, welcome to Cathay 60th year anniversary."為例
text = "Hello, welcome to Cathay 60th year anniversary."
print(count_letters(text))
