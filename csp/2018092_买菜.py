
n = int(input())
a = []
b = []
c = []
d = []
result = 0
for i in range(n):
    ab = list(map(int, input().split()))
    a.append(ab[0])
    b.append(ab[1])
for i in range(n):
    cd = list(map(int, input().split()))
    c.append(cd[0])
    d.append(cd[1])

prec = 0
prea = 0
for i in range(n):
    for j in range(prec, n):
        if (c[i] >= a[j] and c[i] <= b[j]):
            result += (min(b[j], d[i]) - c[i])
            prec = j
            break
    for k in range(prea, n):
        if (a[i] > c[k] and a[i] <= d[k]):
            result += (min(d[k], b[i]) - a[i])
            prea = k
            break
print(result)
