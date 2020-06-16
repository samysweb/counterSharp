int a(int b) {
	return 0;
}

int b(int c) {
	return 1;
}

int test(int c) {
	int b1 = b(c);
	int a1 = a(b1);
	int a2;
	int a3;
	int a4;
	while(0) {
		a1 = a(b1);
	}
	while(0)
		a1 = a(b1);
	
	for(;a1!=a2;)
		a1 = a(b1);
	for(;a1!=a2;){
		a3 = a(b1);
	}

	do
		a1 = a(b1);
	while(0);
	do {
		a(b1);
	} while(0);

	switch(b1) {
		case 10:
			a(b1);
			if (b1==10) {
				a(b1);
			}
			if (__counterSharp_assertMiss==1)
				a(b1);
			else
				a(b1);
		break;
		default:
			a(b1);
			if (b1==10) {
				a(b1);
			}
			if (__counterSharp_assertMiss==1)
				a(b1);
			else
				a(b1);
		break;
	}
	SOMELABEL:
		a(b1);
	return a1;
}