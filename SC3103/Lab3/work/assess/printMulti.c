#include <stdio.h>
#include "mathlib.h"

int main (){
	int num;
	scanf("%d", &num);
	int result;
	result = multiply100(num);
	printf("%d\n", result);
	
	return 0;
}
