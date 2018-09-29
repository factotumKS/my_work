# 二、SML_note2_名字函数和类型

### 2.1 命名常量

​	常量的命名以val关键字开始，以分号结束：

```scheme
val seconds = 60;
```

​	`it`变量总是维持着最近一次输入的表达式的值（包括变量、函数等任意表达式），任何之前的值都会被丢弃。

### 2.2 声明函数

​	函数的命名以fun关键字开始，以分号结束：

```scheme
fun area(r) = pi*r*r;
```

​	上面显然r是形参（formal parameter），等号后面的是函数体（body）；其中形参的括号是可选的，下面的表述也成立：

```scheme
fun area r = pi*r*r;	(*嘻嘻，这是一条注释*)
```

​	**名字的重新声明**，重新给变量名赋予一个新的值并不会报错，这和python是类似的。

### 2.3 标识符

​	表示符（identifier）其实就是“名字”。

​	一个字母名字允许：字母开始，跟随任意数量的字母、数字、下划线、单引号。

​	一个符号名字允许：！ % & $ # + - * / : < = > ? @ \ ~ ` ^ |（注意不要和关键字冲突）。

​	此外下面这些组合是有语法含义的，不能使用：

```scheme
: | = => -> # :>
```



## 数、字符串和真值

### 2.4 算术运算

​	基本运算：加（+），减（-），乘（*），除（div），取模（mod）。

​	负数使用`~`符号单独来表示，注意上面的除法也很特别。

​	科学计数法使用E表示，和C语言类似。

​	**类型约束**，某些函数是**重载**（overloaded，没错就是骨傲天）的，即有不止一个含义。比如加法对两个整数是可用的，对两个浮点数也是可用的，这就存在一种“重载”。重载有的时候需要显式地指出，如：

```scheme
fun square x = x*x;				(*没指明这个函数是给谁用的，被拒绝了*)
> Error~ Unable to resolve overloading for *
fun square x : real = x*x;		(*指明了是实数*)
> val square = fn : real -> real
```

​	类型约束可以出现在函数的任何地方。

​	**默认重载**，表现为上面对类型约束的严格要求，其初衷是允许不同精度的数据同时存在。

​	**标准库**，随便介绍几个了事。

```scheme
Int.abs ~4;
> 4 : int
```

### 2.5 字符串和字符

​	下面介绍一下字符串，还有它相关的的一些函数。

​	连接操作符（^）：将两个字符串首尾相接，如：

```scheme
"yasile" ^ "liangfeifan";
> "yasileliangfeifa" : string
```

​	内置函数size()：接受一个字符串返回里面的字符个数，空格也算哦～。

```scheme
size(it);
> 16 : int
```

​	**特殊字符**，反斜线开始转义序列，和C语言一样。

​	**字符类型**，字符类型（char）和字符串是两回事，用`#`区分它们

```scheme
#"a"	#" "	# "\n"
```

​	str()函数接受一个字符，返回它的字符串版本（char -> string）;

​	String.sub(s, n)函数接受一个字符串，返回字符串s中的第n个字符（string -> char）；

### 2.6 真值和条件表达式

```scheme
if E then E2 else E3	
```

​	关于测试条件E，最简单的就是:

​	（<）：小于；		（>）：大于；

​	（<=）：小于等于；	（>=）：大于等于；

```scheme
fun sign(n) = 
		if n>0 then 1
	else if n=0 then 0
    else (*n<0*) then ~1;
> val sign = fn : int -> int
```

​	测试条件可以用布尔运算组合：

​	（orelse）逻辑或；

​	（andalso）逻辑与；

​	（not，函数）逻辑非；

​	返回布尔值的函数也叫做谓词（predicate），



## 序偶、元组和记录

### 2.7 向量：序偶的例子

​	就是有序二元组啊。

```scheme
(2.5, ~1.2);
> (2.5, ~1.2) : real * real
```

​	序偶也可以作为形参表出现：

```scheme
fun lengthvec (x,y) = Math.sqrt(x*x + y*y);
> val lengthvec = fn real * real -> real
```

### 2.8 多参数和多结果的函数

​	严格来说ML函数其实只具有一个参数和一个返回结果。但是利用元组，函数可以具有多个参数，返回多个结果。

​	**选择元组的分量**，在一个模式上，比如(x,y)，可以通过x和y分别元组的两个分量。

​	**零元组和元组类型**，零元组没有分量，在没有数据传输的时候提供一个占位符。unit类型用于过程性设计，目的是为了“副作用”，传回的总是()，所以这个函数重要的是过程不是目的（笑～）

### 2.9 记录

​	记录是一种分量——称为域（field）——具有标签的元组。

​	元组每个分量是由它所在的位置来标识的。但是记录中的位置是没有意义的。

```scheme
{name="Jones", age=25, salary=15300}
{name="Jones", salary=15300, age=25}
```

​	**记录模式**，如果我们不需要所有的域，可以在其他域所在的地方写三个点（...）,不会揭示其他你不想知道的东西；总之想省略一些域就写（...）

```scheme
val {name=nameV, born=bornV, ...} = henryV;
> bornV = 1387 : int
> nameV = "Henry V" : string
```

​	通过选择符（#）可以从记录里取得给定标签的值。

```scheme
#quote richardIII;
> "Plots have I laid..." : string
```

​	话说标签域也可以是正整数！相应地，使用选择操作符`#k`可以提取n元组中第k个分量的值，如：

```scheme
#2 ("a", "b", 3, false);
> "b" : string
```

​	**部分记录描述**，一个函数只能定义在完整的记录类型上，这是出于安全考虑。

​	**声明记录类型**，在函数的类型约束里面很有用

```scheme
type king = {name	: string,
			born	: int,
            crowned	: int,
            died	: int,
			quote	: string};
> type king
```

### 2.10 中缀操作符

​	中缀操作符（infix operator）是一个写在两个参数中间的函数。

​	使用infix指令可以声明（定义）一个中缀操作符，如异或：

```scheme
infix xor;
fun (p xor q) = (p orelse q) andalso not (p andalso q);
> val xor = fn : (bool * bool) -> bool
```

​	**中缀的优先级**，infix是左结合的，infixr规定是右结合的。每个中缀操作符都有0-9的优先级（比如+的优先级是6），可以指定优先级。

```scheme
infix 6 plus;
fun (a plus b) = "(" ^ a ^ "+" ^ b ^ ")";
> val plus = fn : string * string -> string
```

​	 **隔开符号名字**，符号名字如果连在一起使用会产生很多误会。

```scheme
1+~3;
> Unkown name +~
```

​	**中缀符作为函数**，关键字op覆盖了中缀状态，可以使用`op中缀符`的格式把中缀作为函数使用，可以应用在序偶上。

```scheme
(*这里++已经表示向量加法的中缀符*)
op++ ((2.5, 0.0), (0.1, 2.5));
> (2.6, 2.5) : real * real
op^ ("Mont", "joy");
> "Montjoy" : string
```

​	**取消中缀状态**，对一个自定义的中缀操作符，可以使用`nonfix中缀符`让它回到普通函数的记法。后面的infix指令又可以让它变回去。

```scheme
nonfix *;
3*2;
>Error: Type coflict
*(3,2);
> 6 : int
```



## 表达式的求值

### 2.11 ML中的求值：传值调用

​	对于函数`f(E)`先进行表达式E的求值，再将E的值带入对函数进行计算。

### 2.12 传值调用下的递归函数

​	通常意义下的递归函数需要大量的空间（容易导致栈溢出）。

```scheme
fact(4) => 4 * fact(3)
		=> ...
        => 4 * 3 * 2 * 1 * fact(0)
        => ...
        => 24
(*太多的数等待被乘，浪费空间*)
```

​	**迭代函数**，其实不用囤积大量的待乘数，我们可以立即进行乘法，这样所需要的存储空间就能够固定，不需要溢出，这种技术叫做**尾递归（tail recursive）**，对防止存储空间溢出这非常重要。

```scheme
fact(4,1) => fact(3,4)
		  => ...
          => fact(0,24)
          => ...
          => 24
(*传参的时候就保留单步的计算结果*)
```

​	**条件表达式的特殊作用**，条件表达式允许分情定义，比如阶乘函数：

```scheme
0! = 1
n! = n * (n-1)!
```

​	可以在递归时用`andalso`,`orelse`判断递归。

### 2.13 传需调用或惰性求值

​	传值调用（严格求值）实在是太浪费了，有两种更好的策略。

​	存在一种f(E)的值，直接将E传入f的函数体，然后计算新表达式的值，这称作**传名调用（call-by-name）**。也许传名调用比传值调用节省，但是也未必：

​	还存在一种称为**传需调用（call-by-need，惰性求值）**的方法。它不直接把一个表达式替换到函数体，而是在参数出现的地方用指针链接到表达式上，如果其曾被求值，就共享这个值。指针结构形成了关于函数和参数的有向图。当图的一部分被求值后图会被结果更新，这称为图归约（graph reduction）。

​	然而我们仍然使用严格求值。

​	反正好像每种求值都有自己的漏洞所以这种东西无所谓啦。



## 书写递归函数&局部声明

### 2.14+ 书写递归方程（实例）

​	**局部声明**，使用`let in`语法，如下：

``` scheme
(*约分分数n/d到最简式，使得n和d没有公约数*)
fun fraction (n,d) = 
	let val com = gcd(n,d)	(*最大公约数*)
    in	(n div com, d div com) end;
> val fraction = fn : int * int -> int
```

​	`let D in E end`结构在求值过程中，先对声明D进行求值，并按照结果进行命名，这样的环境仅在这个表达式中是可见的，然后再对表达式E进行求值，并作为整个表达式的值返回。

​	其中let内可以包含复合声明，包含一系列的声明。	

​	**嵌套的函数声明**，以实数平方根的牛顿法为例：

```scheme
fun findroot (a, x, acc) = 
	let val nextx = (a div x + x) div 2.0
    in	if abs (x-nextx) < acc*x	then nextx
        else findroot (a, nextx, acc)
    end;
> val findroot = fn : (real * real * real) -> real
```

​	上面的例子中参数a和acc毫无变化地在每次递归调用中传递着，他们本该是全局的，我们可以加一层`let in`

```scheme
fun sqroot a = 
	let val acc = 1.0E~10
    	fun findroot x = 
        	let val nextx = (a div x + x) div 2.0
   		 	in	if abs (x-nextx) < acc*x	then nextx
        		else findroot (a, nextx, acc)
    		end;
	in findroot 1.0 end;
> val sqroot = fn : real -> real
```

### 2.18 使用local来隐藏声明

​	`local D1 in D2 end`，和let表达式如出一辙。表示D1仅在D2内可见，很少用到，只有在隐藏声明的时候才需要（把D2要用到的D1隐藏起来）。

### 2.19 联立声明

​	联立声明允许同时定义多个名字。

```scheme
val Id1 = E1 and ... and Idn = En
```

​	通常联立是彼此独立的，但是fun声明允许递归，所以可以引入相互递归的函数。

​	**相互递归的函数**，有的函数是相互递归的（mutually recursive），即相互基于对方来递归定义。递归下降语法分析器就是这样的。

​	相互递归的函数通常都可以借助加入一个参数来合并成为一个函数。

​	**仿真goto语句**，好孩子不要学。



## 模块系统初步

### 2.21 结构

​	声明可以被包含在关键字struct和end之间来组合，并使用structure声明来绑定到一个标识符上。

```scheme
(*这个结构定义了复数的性质*)
structure Complex = 
	struct
    type t = real * real;
    val zero = (0.0, 0.0);
    fun sum ((x,y), (x', y')) = (x+x', y+y') : t;
    fun diff ((x,y), (x', y')) = (x-x', y-y') : t;
    fun prod ((x,y), (x', y')) = (x*x' - y*y', x*y' + x'*y) : t;
    ...
    end;
```

​	结构可见时，使用复合名字来访问。

​	与记录相比，记录的组成部分只能是值，而结构的组成部分可以包括类型和异常，但是不能用结构来进行计算。因为只有在程序模块进行连接的时候才会创建结构，结构应该被当作一种封装了的环境。

### 2.22 签名

​	签名是结构里面每一个组件的描述。对结构做出声明之后ML会把相应的签名打印出来作为回应。

```scheme
structure Complex = ...;	(*定义完了*)
> structure Complex :
>	sig
>	type t
>	val diff : (real * real) * (real * real) -> t
>	...
>	end						(*这是系统自动生成的签名体*)
```

​	系统生成的签名未必是我们需要的，比如有的内容其实是私有定义不应该泛用，所以可以**声明签名**，按照自己的需要定义一个签名，下面这个签名把名字ARITH给了sig和end之间的签名：

```scheme
signature ARITH = 
	sig
    type t
    val zero : t
    val sum  : t * t -> t
    val diff : t * t -> t
    val prod : t * t -> t
    val quo  : t * t -> t
    end;
```

​	通过上面这个签名我们可以定义其他的结构，使他们遵守签名，比如下面这个有理数框架：

```scheme
structure Rational : ARITH = 
	struct
    type t = int * int;
    val zero = (0, 1);
    ...
    end;
```

​	签名描述了ML想安全地把程序单元连接起来需要的信息，它可以作为一种定义框架的规则。



## 多态类型检测

​	如果一种对象拥有多种类型，那么它就是**多态**的。

### 2.23 类型推导

​	和python类似，编译器会根据上下文推导，并在出现矛盾的时候报错。

### 2.24 多态函数声明

​	如果类型推导之后还是有一些无约束的类型，那么这个声明就是多态的。

```scheme
fun pairself x = (x, x);
> val pairself = fn 'a -> 'a * 'a
```

​	此处涉及了**类型变量（type variable）**，命名为`'a'`。在ML中类型变量规定以单引号开始。

​	多态类型是一个类型模式。用具体类型去替换类型变量可以形成一个类型模式的实例（instance），所以一个类型模式可以具有无限多的实例。

```scheme
pairself 4.0;
> (4.0, 4.0) : real * real
pairself 7;
> (7, 7) : int * int
```



