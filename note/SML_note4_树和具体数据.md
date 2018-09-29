# SML_note4_树和具体数据

## 数据类型声明

### 4.1 国王与臣民

​	通过数据类型`datatyp`声明创建一个ML类型。

```scheme
datatype person = King
				| Peer of string * string * int
                | Knight of string
                | Peasant of string;
```

​	上面的声明中person表示类型，里面四个部分被称为构造子（constructor）类型person包含且仅包含它构造子所构造的值。King、Peer这些构造子都具有类型person。

​	作用于数据类型之上的函数也可以通过包含构造子的声明来实现跟表函数一样的分情况讨论。

```	scheme
fun title King					= "His Majesty the King"
  | title (Peer(deg, terr, _))	= "The" ^ deg ^ "of" ^ terr
  | title (Knight name)
  | title (Peasant name);
```

### 4.2 枚举类型

​	其中，爵位是有限制的，不是阿猫阿狗都能作为爵位，所以可以引入一种**枚举类型（enumeration type）**，即由有限数目的常量组成的类型。下面degree和爵位都成为了关键字，前者为类型，后者为常量。

```scheme
datatype degree = Duke | Marquis | Earl | Viscount | Baron;
datatype bool = true | false;	(*布尔常量就是一个典型例子*)
```

### 4.3 多态数据类型

​	**可选类型**，类型操作符`option`：

```scheme
datatype 'a option = NONE | SOME of 'a
```

### 4.4 通过val、as、case进行模式匹配

​	**模式（pattern）**，是一个只包含变量、构造子和通配符的表达式。构造子含有：（1）数、字符和字符串常量；（2）序偶、元组和记录结构；（3）表和数据类型的构造子。

​	在模式中，所有不是构造子的名字都是变量，这会取消这些变量在模式之外的意思。

​	`=`在没有`val`的时候会被解读为等于判断，在有val的时候就会变成赋值。

​	**多层模式（layered pattern）**，可以使用`Id as P`这种表达，这样和P绑定的值也会绑定在Id上。

```scheme
fun nextrun (run, [])			 =
  | nextrun (run as r::_, x::xs) =	(*这里run和r::_是同步的*)
  			if x<r then (rev run, x::xs)
  				   else nextrun(x::run, xs);
```

​	