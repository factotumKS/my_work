clc, clear
yx=@(x,y)-2*y+2*x^2+2*x; %定义微分方程右端项的匿名函数
[x,y]=ode45(yx,[0,0.5],1)  %第一种返回格式
sol=ode45(yx,[0,0.5],1)  %第二种返回格式
y2=deval(sol,x)  %计算自变量x对应的函数值
check=[y,y2']  %比较两种计算结果是一样的,但一个是行向量，一个是列向量
