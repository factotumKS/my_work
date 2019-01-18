clc, clear
a(1,2)=2;a(1,3)=8;a(1,4)=1;
a(2,3)=1;a(2,3)=6;a(2,5)=1;
a(3,4)=7;a(3,5)=5;a(3,6)=1;a(3,7)=2;
a(4,7)=9;
a(5,6)=3;a(5,8)=2;a(5,9)=9;
a(6,7)=4;a(6,9)=6;
a(7,9)=3;a(7,10)=1;
a(8,9)=7;a(8,11)=9;
a(9,10)=1;a(9,11)=2;
a(10,11)=4;
a=a';   %matlab工具箱要求数据是下三角矩阵
[i,j,v]=find(a);
b=sparse(i,j,v,11,11) %构造稀疏矩阵
[x,y,z]=graphshortestpath(b,1,11,'Directed',false) % Directed是标志图为有向或无向的属性，该图是无向图，对应的属性值为false，或0。
