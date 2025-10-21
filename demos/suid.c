#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    printf("Real UID: %d\n", getuid());
    printf("Effective UID: %d\n", geteuid());
    setreuid(0, 0);
    system("whoami");
    return 0;
}
