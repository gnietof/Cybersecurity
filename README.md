# Cybersecurity
Cybersecurity materials for leaning and education.

## Wordlists
Lists of common words used for testing passwords strength.

**Note**: The file **common_names.txt** was originally downloaded from [H4CKR Github repository](https://github.com/The-Art-of-Hacking/h4cker) and then all names where converted to lowercase.


## Reference
Different files I found interesting and copied here to prevent them from disappearing from their current sites.

**Note**: The reference for HostApd (WiFi configuration) was originally downloaded from [MIT](https://web.mit.edu/freebsd/head/contrib/wpa/hostapd/hostapd.conf).

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
