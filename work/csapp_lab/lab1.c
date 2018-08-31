#include<stdio.h>


int bitAbs(int x){
	int result = x >> 31; // 符号位扩展，全0全1
	result = (result+x) ^ result; // 正数不变，负数减1取反
	return result;
}

/* 
 * 1、bitAnd - x&y using only ~ and |
 *   Example: bitAnd(6, 5) = 4
 *   Legal ops: ~ |
 *   Max ops: 8
 *   Rating: 1
 *   方法：德摩根律~(x&y)=~x|~y
 */
int bitAnd(int x, int y){
	int z = ~(~x|~y);
	return z;
}

/*
 * 2、getByte - Extract byte n from word x
 *   从字x中提取第n个字节
 *   Bytes numbered from 0 (LSB) to 3 (MSB)
 *   最低有效位为0，依次，最高有效位是 3
 *   Examples: getByte(0x12345678,1) = 0x56
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 6
 *   Rating: 2
 *   方法：默认32位字
 */
int getByte(int x, int n){
	int tmp = (x >> (n<<3)) & 0xff;
	return tmp;
}

/*
 * 3、logicalShift - shift x to the right by n, using a logical shift
 *   逻辑位移，逻辑右移
 *   Can assume that 0 <= n <= 31
 *   Examples: logicalShift(0x87654321,4) = 0x08765432
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 20
 *   Rating: 3
 *   方法：-1左移(32-n)位，得到掩码
 */
int logicalShift(int x, int n){
	int a = (~n) + 1;
	a += 0x20;
	int b = (0xffffffff<<a);
	b = ~b;
	int result = (x>>n)&b;
	return result;
}

/*
 * 4、bitCount - returns count of number of 1's in word
 *   返回 二进制数中 1 的个数
 *   Examples: bitCount(5) = 2, bitCount(7) = 3
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 40
 *   Rating: 4
 *   方法：
 */
int bitCount(int x){
	
}

/*
 * 5、bang - Compute !x without using !
 *   0为1,1为0
 *   Examples: bang(3) = 0, bang(0) = 1
 *   Legal ops: ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 4
 *   方法：两种方法，七步法：求-abs,五步法：如下
 */
int bang(int x){
	int tmp = ~x + 1; //取反加1等于自己的只有0和min值
	tmp = tmp|x;
	int result = tmp>>31;
	return result+1;
}

/*
 * 6、tmin - return minimum two's complement integer
 *   int最小的数
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 4
 *   Rating: 1
 *   方法：送分题
 */
int tmin(){
	return 1<<31;
}
/*
 * 7、fitsBits - return 1 if x can be represented as an
 *  n-bit, two's complement integer.
 *   如果x可以表示为n位二进制补码形式
 *   1 <= n <= 32
 *   Examples: fitsBits(5,3) = 0, fitsBits(-4,3) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 15
 *   Rating: 2
 */
int fitsBits(int x, int n){
	int tmp = x>>n;
	int a = ~(tmp>>31);
	tmp += (a+1);
	tmp = (a+tmp) ^ a;
	tmp = tmp>>31;
	return tmp+1;
}

/*
 * 8、divpwr2 - Compute x/(2^n), for 0 <= n <= 30
 *  计算 x / (2^n)
 *  Round toward zero
 *   Examples: divpwr2(15,1) = 7, divpwr2(-33,4) = -2
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 15
 *   Rating: 2
 */

/*
 * 9、negate - return -x
 *   Example: negate(1) = -1.
 *   求相反数
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 5
 *   Rating: 2
 *   方法：送分题+1
 */
int negate(int x){
	int rx = ~x + 1;
	return rx;
}

/*
 * 10、isPositive - return 1 if x > 0, return 0 otherwise
 *   x > 0 返回1， x <= 0返回0
 *   Example: isPositive(-1) = 0.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 8
 *   Rating: 3
 *   方法：借鉴了bitAbs，实际上有更少的操作数：！((x>>31)|(!x))即可
 *        (FXCK！没看到可以用！运算符)
 */
int isPositive(int x){
	int a = ~(x>>31);
	int result = x + a;
	result = result>>31;
	return (result+1);
}

/*
 * 11、isLessOrEqual - if x <= y  then return 1, else return 0
 *   Example: isLessOrEqual(4,5) = 1.
 *   x - y <= 0返回1，  > 0返回0
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 24
 *   Rating: 3
 *   方法：下面的方法在y=min值的时候是错误的
 */
int isLessOrEqual(int x, int y){
	int a = ~y+1;
	int z = x + a;
	int result = z>>31;
	result = (~result+1)|(!z);
	return result;
}
/*
 * 12、ilog2 - return floor(log base 2 of x), where x > 0
 *   Example: ilog2(16) = 4  即得到由多少位二进制表示即可。
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 90
 *   Rating: 4
 *   方法：参考。二分法。先右移16位后若大于0即得到（10000)2=16
 *   否则得到0，判断最高位是否为0，若不为0，则包含2的16次方。即得到最高位的log  *    数，同理其他
 */
int ilog2()

/*
 * 13、float_neg - Return bit-level equivalent of expression -f for
 *   floating point argument f. 返回和浮点数参数-f相等的二进制
 *   Both the argument and result are passed as unsigned int's, but
 *   they are to be interpreted as the bit-level representations of
 *   single-precision floating point values.
 *   参数和返回结果都是无符号整数，但是可以解释成单精度浮点数的二进制表示
 *   When argument is NaN, return argument.
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 10
 *   Rating: 2
 */

/*
 * 14、float_i2f - Return bit-level equivalent of expression (float) x
 *  返回int x的浮点数的二进制形式。
 *   Result is returned as unsigned int, but
 *   it is to be interpreted as the bit-level representation of a
 *   single-precision floating point values.
 *   返回的是unsigned型但是表示的时二进制单精度形式
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 4
 */

/*
 * 15、float_twice - Return bit-level equivalent of expression 2*f for
 *   floating point argument f.
 ×   返回 以unsinged表示的浮点数二进制的二倍的二进制unsigned型
 *   Both the argument and result are passed as unsigned int's, but
 *   they are to be interpreted as the bit-level representation of
 *   single-precision floating point values.
 *   When argument is NaN, return argument
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 4
 */


void main(){
	printf("test bitAbs: 1->%d -1->%d 0->%d\n",
		   bitAbs(1), bitAbs(-1), bitAbs(0));
	printf("test bitAnd(6,5): %d\n",
		   bitAnd(6, 5));
	printf("test getByte(0x12345678,1): %d\n",
		   getByte(0x12345678,1));
	printf("test logicalShift(0x12345678,4): %x\n",
		   logicalShift(0x12345678,4));
	printf("test bang(3): %d and bang(0): %d\n",
		   bang(3),bang(0));
	printf("test fitsBits(5,3): %d and fitsBits(-4,3): %d\n",
		   fitsBits(5,3), fitsBits(-4,3));
	printf("test negate(3): %d\n",
		   negate(3));
	printf("test isPositive(3): %d, isPositive(0): %d\n",
		   isPositive(3),isPositive(0));
	printf("test isLessOrEqual(4,5): %d, isLessOrEqual(6,3): %d\n",
		   isLessOrEqual(4,5),isLessOrEqual(6,3));
	return;
}
