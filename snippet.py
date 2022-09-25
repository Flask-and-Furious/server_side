def series_sum(n):
    sum = 0
    for i in range(1, n + 1):
        sum += 1 / i
    sum = str(round(sum, 2))
    if n == 0:
        return '0.00'
    return sum

# 1 => '1.00' (1)                  
# 2 => '1.5' (1 + 1/2)
# 5 => '2.28' (1 + 1/2 + 1/3 + 1/4 + 1/5)
# If the given value is 0,
# it should return '0.00'