#include <stdio.h>
#define GOODS 3
#define VOLUME 50

void quick_sort(int* w; int* p; int num);

void main()
{
	int weight[GOODS];
	int price[GOODS];
	int i;
	for(i=0; i<GOODS; i++)	//输入各物品的重量和价格
	{
		printf("%d", i);
		scanf("Please enter the weight and price:", weight+i, price+i);
	}
	quick_sort(weight, price, GOODS);	//对重量和价格序列进行排序
	
	int c[GOODS][11];
	for(i=0; i<11; i++)	//表格初始化
	{
		c[0][i] = 0;
	}
	for(i=1; i<(GOODS+1); i++)
	{
		int j;
		for(j=0; j<11; j++)
		{
			int plan1;
			int plan2;
		}
	}
}

void quick_sort(int* w; int* p; int num)
{
	
}