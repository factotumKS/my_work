## 时间延迟

​	带时延的连续赋值语句

```verilog

//#2指两个时间单位
assign #2 Sum = A^B
```

​	没有说明时延单位，会有缺省值。

## 模块

```verilog

module mux2_1(out1, a, b, sel);
	output out1;
	input a, b, sel;

//描述模块中各门的输入输出
not(sel_, sel);
and(a1, a, sel_);
and(b1, b, sel);
or(out1, a1, b1);

endmodule
```

```verilog

//数据流描述
assign out1 = (sel & b)|(~sel & a);
```

​	可以对组合、时序逻辑电路建模。
```verilog

//行为描述
always @(sel or a or b)
begin 
    if(sel)
        out1 = b;
    else
        out1 = a;
end
```

​	**结构**和**行为**描述方式可以自由混合。

```

```

