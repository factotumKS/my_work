# note2_自制编译器

## 1、语法分析概要

​	词法分析、语法分析、语义分析分成三个模块是理想状态，实际实现按照方便的形式来。

### 1.1、扫描器，scanner

​	有的token有语义值（semantic  value），“54”的语义为“数值  54”；不过不绝对，“int”就不需要。

#### 1.1.1、token

​	具有种类、语义值两个特征，有的token没有语义值（semantic  value），“54”的语义为“数值  54”；“int”就不需要。



### 1.2、解析器生成器

​	一般来说可处理的语法范围和解析速度成反比。其中LL非常窄，但是处理速度非常快。

​	使用JavaCC作为解析器生成器，它属于LL类型的。

​	JavaCC是解析器生成器，同时也是扫描器生成器。

#### 1.2.1、语法描述文件

​	语法规则通常会用一个扩展名为“.jj”的文件来描述，该文件称为语法描述文件。

```java
options {
    JavaCC的选项
}
PARSER_BEGIN(解析器类名)
package 包名;
import 库名;

public class 解析器类名 {
	任意的Java代码
}
PARSER_END(解析器类名)

扫描器的描述

解析器的描述
```

#### 1.2.2、语法描述文件例子

```
options {
    STATIC = false;
}
PARSER_BEGIN(Adder)
import java.io.*;
class Adder {
    static public void main(String[] args) {
        for (String arg : args) {
            try {
                System.out.println(evaluate(arg));
            }
            catch (ParseException ex) {
                System.err.println(ex.getMessage());
            }
        }
    }
    static public long evaluate(String src) throws ParseException {
        Reader reader = new StringReader(src);
        return new Adder(reader).expr();
    }
}
PARSER_END(Adder)
SKIP: { <[" ","\t","\r","\n"]> }
TOKEN: {
    <INTEGER: (["0"-"9"])+>
}
long expr():

```



