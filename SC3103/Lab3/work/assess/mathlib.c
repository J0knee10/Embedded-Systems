#include "mathlib.h"

int fact(int n){
	if (n <= 1){
		return 1;
	}
	return (n * fact(n-1));
}

int multiply100(int n){
	return (n * 100);
}
