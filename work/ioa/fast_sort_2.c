#include<stdio.h>
#include<stdlib.h>

void fast_sort(int* A, int* p, int* r);
int* part(int* A, int* p, int* r);

void main(){
	int A[] = {6,8,7,5,4,1,0,3,2,9};
	for(int i=0; i<10; i++){
		printf("%d ",*(A+i));
	}
	printf("\n");
	fast_sort(A, A, A+9);
	for(int i=0; i<10; i++){
		printf("%d ",*(A+i));
	}
	printf("\n");
	return;
}

void fast_sort(int* A, int* p, int* r){
	if(r > p){
		int* q = part(A, p, r);
		fast_sort(A, p, q-1);
		fast_sort(A, q+1, r);
	}
}

int* part(int* A, int* p, int* r){
	
	//if(*m != *r){
	//	*m ^= *r;
	//	*r ^= *m;
	//	*m ^= *r;
	//}
	int* i = p-1;
	for(int*j=p; j <r; j++){
		if(*j <= *r){
			i++;
			int tmp = *j;
			*j = *i;
			*i = tmp;
		}
	}
	i++;
	int tmp = *i;
	*i = *r;
	*r = tmp;
	return i;
}

