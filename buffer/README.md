# Buffer Overflow

This example is based on the tutorial published here: https://valsamaras.medium.com/introduction-to-x64-linux-binary-exploitation-part-1-14ad4a27aeef
The main difference is that this page covers 64bit operating system explotaitation.

There are several files in this repository.

1. *payload.txt*. File including the payload required to open a shell when exploiting the buffer overflow.
1. *over.c*. Source code for the vulnerable C application.
1. *loader.py* A simple Python script which creates the crafted input for the vulnerable application. This script accepts three parameters:
   - Size of the payload based on the size of the buffer which has to be overflowed.
   - Pointer which will be placed on the stack which points to our overflowed content.
   - Optionally, a file name where this payload will be placed.
   
The code included here requires that a lot of the current protections included in latest versions of the operating system are removed. And even then, the required SUID bit is not honored. 
I have been able to explot the vulnerability ... inside GDB. I have not been able to reproduce the vulnerability in the command line.
