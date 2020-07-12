#include<assert.h>
#include<malloc.h>
#include "malloc.h"

char __counterSharp_status=0;

int test2(int sum) {
	for (int i=0; i<32; i++) {
        sum+=i;
    }
	return sum;
}

int test(int someInput) {
	int *someMemory = malloc(sizeof(int));
    int sum = 0;
    for (int i=0; i<10; i++) {
        sum+=i;
    }
	sum = test2(sum);
	__counterSharp_assert(someInput!=1);
    //__counterSharp_assert(someInput>1024 || someInput<-1024);
	//__counterSharp_assert(someInput*(*someMemory)!=0);
	if (someMemory==20) {
		return 19;
	} else {
		return 10;
	}
}