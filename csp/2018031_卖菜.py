#常用输入输出格式
a = list(map(int,input().split()))
b = 0

pre = 1
for i in range(len(a)-1):
    if (a[i] == 1):
        pre = 1
        b += 1
    elif (pre == 1):
        pre = 2
        b += 2
    else:
        pre += 2
        b += pre

print(b)
