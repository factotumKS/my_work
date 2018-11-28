# note1-自制编译器

## 1、可执行文件

​	linux上的可执行文件都符合ELF规范，包含了程序（代码）以及如何运行该程序的相关信息（元数据）。



## 2、语法

### 2.1、关键字import

​	导入文件代替include，类似python



## 3、编译器构成

### 3.1、包

​	compiler包中包含统领全局的Compiler类，一些语义分析类还有生成中间代码的类，编译器对象可以生成出来

### 3.2、范型，JAVA5

​	不同对象的列表

```java
		//List<类型名>
		List<SourceFile>
```

### 3.3、语句，foreach

​	遍历可迭代对象的

```java
        for (SourceFile src : srcs) {
            compile(src.path(), opts.asmFileNameOf(src), opts);
            assemble(src.path(), opts.objFileNameOf(src), opts);
        }
```



### 3.4、实现compile函数

```java
    public void compile(String srcPath, String destPath,
                        Options opts) throws CompileException {
        //parse:语法分析，生成抽象语法树
        AST ast = parseFile(srcPath, opts);
        TypeTable types = opts.typeTable();
        //语义分析
        AST sem = semanticAnalyze(ast, types, opts);
        //生成中间代码，是IR对象，到这里是前端部分
        IR ir = new IRGenerator(errorHandler).generate(sem, types);
        //生成汇编语言（隐藏优化成分）
        String asm = generateAssembly(ir, opts);
        //写入文件
        writeFile(destPath, asm);
    }
```

