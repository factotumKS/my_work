# SML_note3_表

## 表的介绍

表是一个有序的元素序列，元素可以重复出现，必须是同一类型。

### 3.1 表的构造

表有两个“原语”：`nil`和`::`，

`nil`是空表，也写作`[]`，`nil=[]`；

`::`的意思是构造（construct），接受表头h和表尾t构建一个表`h::t`，表头是一个元素，而表尾本身也得是个表。（表的操作不对称，前面的元素更容易到达，所以这玩意儿是个链表不是个哈希表啊！）

### 3.2 表的操作

以一个找到表中最小元素的递归函数为例：

```scheme
fun minl [m]		= m
  | minl (m::n::ns) = if m>n then minl(n::ns)
  							 else minl(m::ns);
> ***Warning: Matches are not exhaustive
> val minl = fn int list -> int
```

这个函数分两种情况来处理，使用`|`来分开，警告是因为这个函数对空表是没有定义的，这种时候会：

```scheme
minl [];
> Exception: Match	(*出现了一个Match异常*)
```

异常（exception）在这里是一个运行错误后面会讲如何捕获异常。

**中间表、临时表**，计算过程中可能会生成和使用一些表。对于这种我们可以尽量隐藏递归过程。比如，可以用prod函数和upto函数来定义阶乘，前者把每一个元素相乘，后者会返回一个依次加一的列表：

```scheme
fun factl (n) = prod (upto (1,n));
> val factl = fn : int -> int
```

不过缺点是比较抽象，不能体现原本函数的意义。
**字符串和表**，字符串和“字符的表”之间也有explode函数和implode函数来转换。

```scheme
explode "Banquo";
> [#"B", #"a", #"n", #"q", #"u", #"o"] : char list
implode it;
> "Banquo" : string
```

## 基本的表函数

### 3.3 表的测试和分解

（1）、`null`：接受一个表，返回其是否为空表。`_`给那些不关心的变量命名，是一个（所谓的）通配符。

```scheme
fun null   []	= true
  | null (_::_) = false;
> val null = fn : 'a list -> bool
```

（2）`hd`：接受一个非空表，返回其表头元素。注意这个函数不检查是否为非空表。

```scheme
fun hd (x::_) = x;
```

（3）`tl`：接受一个非空表，返回表尾。也不检查。

```scheme
fun tl (_::x) = x;
```

通过上面这三个函数，就不需要再使用模式匹配了。

### 3.4 与数量有关的表处理

（1）`length`：接受一个表，返回表的长度（递归实现）。

先给出一个朴素版本nlength，这个版本的缺点是典型的递归缺点，即占用空间太大，容易导致栈溢出，这在应用于一个长表时十分明显。

```scheme
fun nlength []	    = 0
  | nlength (x::xs) = nlength(xs) + 1;
```

所以我们给出一个实用版本length，这里使用了原来提到的一种**尾递归**技巧。

```scheme
local
	fun addlen (n, []) = n
      | addlen (n, (x::xs)) = addlen(n+1, xs);
in
	fun length(l) = addlen(0, l)
end;
```

​	（2）`take`：接受一个表l和一个数字i，返回表l的前i个元素组成的表。

​	同上使用的是尾递归技巧。

```scheme
fun rtake ([], _, taken)	= taken
  | rtake (x::xs, i, taken) =
  		if i>0 then rtake(xs, i-1, x::taken)
        	   else 	
```

​	注意上面的代码只是把表分成两个部分，这个分界线不断地在移动，函数很好，只是结果是倒的，效果和**栈**类似。

​	不过这里用递归版本也是没关系的！！！回想一下主方法，如果构造新表的代价超过了递归深度导致的代价，那么递归也没关系！！！

​	（3）`drop`：接受一个表l和一个数字i，返回第去掉前i个元素之后的表，即从i+1号元素开始的表。

```scheme
fun drop ([], _)	= []
  | drop (x::xs, i) = if i>0 then drop (xs, i-1)
  							 else x::xs;
```

### 3.5 追加和翻转

​	（1）`@：追加操作`：使用`@`操作符可以把两个表首尾相接形成一个新表，这里也是递归定义的，不需要使用迭代版本。

​	对于xs@ys，计算过程中会把xs拆解成用`::`连接的格式并一一加入ys中，所以时间仅仅与xs有关，这一部分原因也是ML中表结构是用链表存储导致的。

​	（2）`rev`：接受一个表，返回这个表的逆序版本。下面给出一个时间复杂度为O(n^2)的版本：

```scheme
fun nrev []		 = []
  | nrev (x::xs) = (nrev xs) @ [x];		（*这里的@挺浪费*）
```

​	我们可以使用栈结构来翻转表，即递归性地把表头元素加在另一表上，这样时间复杂度就降为O(n)：

```scheme
local 
	(*这个函数递归性地取出xs的表头加在ys上*)
	fun revAppend ([], ys) = ys  	  | revAppend (x::xs, ys) = revAppend(xs, x::ys)
in
    fun rev xs = revAppend(xs, [])
end;
```

### 3.6 表的表、序偶的表

​	（1）`concat`：接受一个表的表，把子表使用`@`连接起来。

```scheme
fun concat [] 	   = []
  | concat (l::ls) = l @ concat ls;
```

​	（2）`zip`：接受两个表，把两个表中的元素依序两两配对组成序偶，并返回一个由序偶组成的表。如果两个表长度不等，会自动忽略多余的元素。整个过程就像拉上拉链一样。

```scheme
fun zip (x::xs, y::ys) = (x,y) :: zip(xs, ys) 
  | zip _			   = [];
```

​	上面的第二种情况可以匹配所有的情况，但是按照顺序，只有不满足第一种情况才会判断第二种。

​	（3）`unzip`：即zip的反函数，把序偶的表转化成为表的序偶。

```scheme
fun unzip [] = ([], [])
  | unzip ((x,y)::pairs) = 
  		let val (xs, ys) = unzip(pairs)
        in (x::xs, y::ys) end;
```



​	