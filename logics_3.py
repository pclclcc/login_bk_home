""" logics_3.py"""

def list_to_specified_number(number):
  """
  依指定規律列出到指定位數的列表

  Args:
    number: 要列出的項數

  Returns:
    a_list: 計算後的數列
  """

  # 初始數列

  a_list = [0, 1]

  # 計算後續項數
  n = number
  # 從a3開始
  for i in range(2, n):
    # a[i] = a[i-1] * (a[i-2]+1)
    a_list.append(a_list[i-1] * (a_list[i-2]+1))

  # 回傳數列

  return a_list

def max_under_limit(limit):
  """
  計算出到限制值以內的最大值和其項數為何

  Args:
    limit: 限制值

  Returns:
    max: 限制內的最大數值
    number: max的項數
  """

  # 初始化數列

  a = [0, 1]

  # 計算後續項數
  i = 2

  while a[i-1] < limit:
    # a[i] = a[i-1] * (a[i-2]+1)
    a.append(a[i-1] * (a[i-2]+1))
    if a[i] > limit:
      break
    i += 1
  max = a[i-1]
  number = i
  # 回傳最大值和項數
  return max, number

number = 13
limit = 1000

print(f"前{number}項:", list_to_specified_number(number))
print(f"小於{limit}的最大數為:{max_under_limit(limit)[0]}位於第{max_under_limit(limit)[1]}項")