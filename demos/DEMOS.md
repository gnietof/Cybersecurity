# Demos

## SUID Demo

In order to test the use of the SUID bit:

- Compile the suid.c file included with:
```bash
gcc suic.c -o suid
```
- Execute and see that the effective user is the user.
- Change the owner with :
```bash
sudo chown owner:owner suid
```
- Execute and see that the effective user is the user.
- Activate the SUID bit with:
```bash
sudo chmod 4755 suid
```
- Execute and see that the effective user is **root**!.

## John the ripper

To make a small demo on how easy is to crack a password:

- Install the ripper:
```bash
sudo apt-get install john
```
- Create a new user in the Linux system
```bash
sudo chmod 4755 suid
```
