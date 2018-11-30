"""
n = int(input())

prePrices = input().split(" ")
prePrices = list(map(int, prePrices))
newPrices = []

newPrices.append((prePrices[0] + prePrices[1]) // 2)
for i in range(1, n-1):
    newPrices.append((prePrices[i-1] + prePrices[i] + prePrices[i+1]) // 3)
newPrices.append((prePrices[-1] + prePrices[-2]) // 2)
                    
newPrices = list(map(lambda x : str(int(x)), newPrices))
print(" ".join(newPrices))
"""
#感觉自己太菜了，不是很熟悉输入输出，python的一些特性也不是很了解
#卖菜
#输入
n = int(input())
a = list(map(int,input().split()))
b=[]
#计算第二天菜价
for i in range(n):
    if(i==0):
        b.append((a[0]+a[1])//2)
    elif(i==n-1):
        b.append((a[-2]+a[-1])//2)
    else:
        b.append((a[i-1]+a[i]+a[i+1])//3)
#输出
print(" ".join(map(str,b)))