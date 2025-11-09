# VulnHub

## Troll3
- Hago un port scan con NMap (nmap -sV -O -n 192.168.161.0/24) para ver qué equipos y que puertos/servicios tienen levantados. La máquina Troll3 tiene levantado sólo el puerto 22.
<img width="709" height="213" alt="image" src="https://github.com/user-attachments/assets/7e590e5f-178b-4678-9b37-d9012ca14609" />

- Realmente no sería necesario porque al poner en marcha la máquina virtual me indica que me conecte directamente con el usuario **start** y la contraseña **here**. Así que, a pesar del inconveniente del teclado, puedo trabajar directamente desde la máquina. Al menos de momento.
<img width="546" height="109" alt="image" src="https://github.com/user-attachments/assets/a3834d6d-bdfd-46b9-b3ec-d2a7f1bc35c6" />

  
- Ya que estoy dentro de la máquina, saco una lista de usuarios haciendo un *cat* del fichero /etc/passwd. No sé si me será de mucha ayuda pero ...
<img width="714" height="597" alt="image" src="https://github.com/user-attachments/assets/ab1f924f-c592-4ad8-bc8d-a09c44844f1a" />

- Y vuelco la lista de nombres de usuario a un fichero por si los necesito.
```bash
cat /etc/passwd | awk -F: '{print $1}' > users.txt
```

- A continuación inspecciono el contenido del directorio del usuario start. Encuentro dos directorios con un fichero en cada uno.
<img width="584" height="119" alt="image" src="https://github.com/user-attachments/assets/14d27cbc-e599-49b7-b732-4d5d5627480a" />

- Miro el contenido de los ficheros. En uno una URL acortada y en el otro una contraseña.
<img width="412" height="87" alt="image" src="https://github.com/user-attachments/assets/a9614d8c-7ae0-4db3-8921-21212238e95e" />

- En la URL encuentro esta página (navegando desde la máquina Host). Pero después de probar varias cosas (incluido el teclear **ferguson clean up** no veo nada. 
<img width="1144" height="568" alt="image" src="https://github.com/user-attachments/assets/e141fa2e-ab36-43a1-be56-43c479a7bd6d" />

- Abandono este camino por ahora y me vuelvo al terminal de la máquina virtual. Vuelco el contenido de **/etc/hosts** y veo que tiene definida la dirección 127.0.1.1.
<img width="507" height="169" alt="image" src="https://github.com/user-attachments/assets/ac25d0da-3bb6-4327-9d55-a350da098391" />

- Hago un ping a esa dirección y veo que responde. 
<img width="502" height="167" alt="image" src="https://github.com/user-attachments/assets/de5cf887-aa93-4701-abfa-1066a4235fae" />

- Pero intento hacer un ssh y parece que no hay nada. Luego volveré.
<img width="802" height="456" alt="image" src="https://github.com/user-attachments/assets/b11973da-a4ce-4eb0-b986-fc74167e016c" />

- Compruebo qué puertos abiertos tiene la máquina. No veo nada especial más que ese 127.0.0.53:53 y 0.0.0.0:68 (udp) pero parece que es normal para DNS y DHCP. 
```bash
netstat -lntu
```
<img width="633" height="151" alt="image" src="https://github.com/user-attachments/assets/57cfbd4c-a783-4f17-9aec-e982a0ad8e0a" />

- Después de probar varias cosas más veo que hay una entrada *extraña* en el directorio home del usuario start.  
<img width="473" height="263" alt="image" src="https://github.com/user-attachments/assets/4330f21f-566c-495a-9a9e-b2f78d396889" />

- Entro en ese directorio y listo los contenidos. Encuentro un fichero con otro usuario y contraseña.
<img width="439" height="149" alt="image" src="https://github.com/user-attachments/assets/38938e38-b24a-49a8-b6ca-b9ccd29c9d91" />

- Hago un *su* con ese usuario y contraseña pero no veo nada especial.
<img width="522" height="162" alt="image" src="https://github.com/user-attachments/assets/e1b64632-26e3-4562-bdb9-a667c6f3b843" />



