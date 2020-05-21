#include<assert.h>
#include<malloc.h>

char __counterSharp_status=0;

int test(int someinput) {
    int *someMemory = malloc(sizeof(int));
    int sum = 0;
    // Wrong summation due to start at 0
    for (int i=0; i<10; i++) {
        sum+=i;
    }
    // Might yield division by zero
    //int test=sum/(someinput*(*someMemory));
	if (someinput<0) {
		someinput=0;
	}
    if ((someinput*(*someMemory))==0) {
		__counterSharp_status=1;
		goto __counterSharp_result;
	}
	__counterSharp_result:
	assert(0);
}