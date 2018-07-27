#include<stdio.h>


int bitAbs(int x){
	int result = x >> 31; // 符号位扩展，全0全1
	result = (result+x) ^ result; // 正数不变，负数减1取反
	return result;
}

/*
 * bitAnd - x&y using only ~ and |
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
 * getByte - Extract byte n from word x
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
 * logicalShift - shift x to the right by n, using a logical shift
 *   逻辑位移，逻辑右移
 *   Can assume that 0 <= n <= 31
 *   Examples: logicalShift(0x87654321,4) = 0x08765432
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 20
 *   Rating: 3
 */
int logicalShift(int x, int n){
	int a = (~n) + 1;
	a += 0x20;
	int b = (0xffffffff<<a);
	b = ~b;
	int result = (x>>n)&b;
	return result;
}
 
void main(){
	printf("test bitAbs: 1->%d -1->%d 0->%d\n",
		   bitAbs(1), bitAbs(-1), bitAbs(0));
	printf("test bitAnd(6,5), expect 4: %d\n",
		   bitAnd(6, 5));
	printf("test getByte(0x12345678,1): %d\n",
		   getByte(0x12345678,1));
	printf("test logicalShift(0x12345678,4): %x\n",
		   logicalShift(0x12345678,4));
	return;
}
