# Demos

## Birthday Demo

# Birthday Demo
Esta es una demostración de cómo se puede conseguir una colisión entre dos cadenas diferentes de manera que generen hash MD5 que coincidan hasta un número determinado de posiciones. 

En un equipo en el que tengamos instalado Python y Pip, necesitamos instalar las librerías PyCrypto

```bash
pip install pyCrypto
```

Lo ejecutamos y proporcionamos dos cadenas de caracteres e indicamos con cuantos caracteres queremos que coincidan los dos Hash.
Yo he probado con Genaro Nieto, Luis Crespo y 6 caracteres y al cabo de unos 80 segundos (en una VMWare Ubuntu con 4GB de RAM y dos procesadores) me ha dado.

```bash
 Simple Collision Test
 =-==-==-==-==-=
To be hashed: Genaro Nieto
To preceed: Luis Crespo
To how many places? 6
Total Attempts: 12751416 / Took 81.24 seconds
Nonce: 12751417
23280161e8a3e3bbb89aeac858e1c8a7
23280161e8a3e3bbb89aeac858e1c8a7
```

Ahora lo comprobamos. Para ello necesitamos tener instalado en el ordenador el comando md5.

```bash
sudo apt-get update
sudo apt-get install coreutils
```
Y hacemos un md5sum con cada una de las cadenas añadiéndoles el _Nonce_ que hemos obtenido:

```bash
printf 'Genaro Nieto12751417' | md5sum
23280161e8a3e3bbb89aeac858e1c8a7  -
printf 'Luis Crespo12751417' | md5sum
232801a68d8774f6d464b32d5a0a39ae  -
```
Vemos que, efectivamente, coinciden las seis primeras posiciones.

Como curiosidad, he lanzado este script con las mismas cadenas de entrada pero pidiendo una coincidencia de 10 caracteres.

```bash
```

Un hash MD5 tiene 128 bits (o 32 caracteres hexadecimales). Si para que coincidan 6 caracteres ha tardado 80 segundos y para 10 caracteres xx segundos.  

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
