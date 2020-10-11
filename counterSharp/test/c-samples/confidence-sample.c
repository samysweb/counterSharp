#include<assert.h>
#include<malloc.h>
#include "malloc.h"

char __counterSharp_status=0;

int test(int someInput) {
	__counterSharp_assume(someInput>0);
	int sum = 0;
	if (someInput>8) {
		for (int i=1; i<=someInput; i++) {
			sum+=i;
		}
	}
	__counterSharp_assert((someInput*(someInput+1))/2==sum);
    //__counterSharp_assert(someInput>1024 || someInput<-1024);
	//__counterSharp_assert(someInput*(*someMemory)!=0);
}