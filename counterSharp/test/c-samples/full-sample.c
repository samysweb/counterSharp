#include<assert.h>
#include<malloc.h>
#include "malloc.h"

char __counterSharp_status=0;

int test(int someInput) {
	__counterSharp_assume(someInput<100 && someInput>-100);
    int *someMemory = malloc(sizeof(int));
    int sum = 0;
    for (int i=0; i<10; i++) {
        sum+=i;
    }
	for (int i=0; i<32; i++) {
        sum+=i;
    }
    __counterSharp_assert(someInput*(*someMemory)!=0);
	__counterSharp_assert(someInput*(*someMemory)!=2);
	return test(10);
}