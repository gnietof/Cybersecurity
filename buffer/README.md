# Buffer Overflow (Work in progress)

This example is based on the tutorial published here: https://valsamaras.medium.com/introduction-to-x64-linux-binary-exploitation-part-1-14ad4a27aeef.  
The main difference with other tutorials is that this one covers 64bit operating system explotaitation.

There are several files in this repository.

1. *payload.txt*. File including the payload required to open a shell when exploiting the buffer overflow.
1. *over.c*. Source code for the vulnerable C application.
1. *loader.py* A simple Python script which creates the crafted input for the vulnerable application. This script accepts three parameters:
   - Size of the payload based on the size of the buffer which has to be overflowed.
   - Pointer which will be placed on the stack which points to our overflowed content.
   - Optionally, a file name where this payload will be placed.
   
The code included here requires that a lot of the current protections included in latest versions of the operating system are removed. And even then, the required SUID bit is not honored. 
I have been able to explot the vulnerability ... inside GDB. I have not been able to reproduce the vulnerability in the command line.

## Steps

1. Deactivate the randonmization of memory addresses.
```bash
sudo sysctl kernel.randomize_va_space=0 
```
2. Install gcc which is not included by default in Ubuntu Desktop.
```bash
sudo apt-get update && sudo apt-get install gcc
```
3. Install the GEF extension for GDB
```bash
$ bash -c "$(wget https://gef.blah.cat/sh -O -)"
```
4. Compile the source code.
```bash
gcc -g -fno-stack-protector -z execstack -o over over.c
```
5. Set root as owner of the executable. Activate execution and the SUID bit.
```bash
sudo chown root:root over
sudo chmod +s over
```
Activate execution if required.
```bash
sudo chmod +x over 
```
Prepare the payload we will be providing as input to the executable.
```bash
python3 ./loader.py 208 
```

```bash
```
Breakpoint at main
b main
Check function1 return
disas function1

