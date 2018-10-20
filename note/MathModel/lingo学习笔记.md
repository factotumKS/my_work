# lingo学习笔记

​	

​	程序范例

```matlab
! 这是一个分配问题的程序
model:
sets:
var/1..5/;
links(var, var):c, x;
endsets

data:
c = 3 8 2 10 3
    8 7 2 9 7
    6 4 2 7 5
    8 4 2 7 5
    9 10 6 9 10;
enddata

max = @sum(links:c*x);
@for(var(i):@sum(var(j):x(i,j)) = 1);
@for(var(i):@sum(var(j):x(j,i)) = 1);
@for(links:@bin(x));
```

​	至少分为sets、data、问题两个部分。



## 1、集合（sets）

​	sets到endsets之间声明了一系列集合，集合有自己的元素，还有自己的属性。

```matlab
sets:
集合/集合元素/:集合属性;
endsets
```

​	lingo所有的操作都是建立在集合上面的，@for遍历一个集合里面的所有元素，@sum是遍历元素带入表达式并求和。