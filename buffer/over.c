#include <string.h>
#include <stdio.h>

void overflowed() {
	printf("%s\n", "Execution Hijacked");
}

void function1(char *str){
	char buffer[200];
	strcpy(buffer, str);
	printf("Input: %s",buffer);
}

int main(int argc, char *argv[]) {
	function1(argv[1]);
	printf("%s\n", "Executed normally");
	return 0;
}

