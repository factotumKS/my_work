# haskell-note1

## 一、基本语法

​	与函数式语言sml类似有部分函数调用可以写为中缀形式。

```haskell
--算数运算--
+ - * /
--等与不等--
== /=
```

​	优先级：函数调用优先级最高，可以使用括号指定优先级。

```haskell
--简单的函数mysquare.hs--
maysquare x = x * x
```

​	分支：注意haskell中else是不可省略的，（比较老的语言比如C，可以省略else可能是出于代码文本占用空间的考虑，就像用++取代+=1一样，并不是个好设计）

```haskell
if then else
```



## list类型

​	