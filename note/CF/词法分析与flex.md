# 词法分析与flex

## 1、安装与使用flex

​	安装：

```bash
$ sudo pacman -S flex
```

​	按照flex规范，编写源文件，为`.l`后缀；然后用flex进行编译，得到相应C程序`lex.yy.c`。

```bash
$ flex scanner.l
```

​	编译得到的文件可以用gcc。

```bash
$ gcc lex.yy.c -o scanner
```

​	分析文件时的命令

```bash
$ ./scanner input.txt
```





## 2、语法

```C
{definitions}
%%
{rules}
%%
{user subroutines}
```



### 2.1、声明部分，definitions

​	声明正则表达式，需要按照正则表达式的语法规范。

```C
{
	表达式名称	表达式
}
```

​	例子：

```C
INT	[1-9][0-9]*[0]	//0或不以0开头的由0-9组成的字符串
FLOAT [0-9]*[.][0-9]+([eE][+-]?[0-9]*|[0])?f?    //浮点数
```



### 2.2、规则部分,rules

​	制定规则，规定匹配到字符串之后的行为：

```
{LABEL1} |
{LABLE2} |
...
{ 
/*TODO*/
}
```

​	例子：

```C
//打印匹配到的整数
{INT}{
    printf("Pick up an integer, value is %d", atoi(yytext));
    printf("Pick up an integer, value is %s", yytext);
}
```

#### 2.2.1、匹配规则

​	对于一个串，尝试所有规则，如果匹配长度不等就取长者；如果长度相等就取第一个。

#### 2.2.2、状态机

​	根据之前遇到的不同token，有必要做出不同的行为；这可以用全局变量实现。



### 2.3、用户项目，user subroutines

​	写下用户需要执行的C语言代码。这部分会无改动地被写入`lex.yy.c`。

​	这部分可以用来写main函数，也可以用来写自己的函数，如下面这个实例

```C
//这个函数会把所有的jojo替换成dio
%option main //生成main函数
//全局定义
%{
int kono();
%}

%%
jojo {kono();}

%%
int kono(){
    printf("dio");
    return 0;
}
```



## 3、其他要点

### 3.1、字符串表，String Table

​	一些token可能会重复出现，需要制作一个表保存信息，节省时间空间。



## 4、实例

​	来尝试着写一个C语言的scanner