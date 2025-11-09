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

- Siguiendo lo que sugerían en algún sitio me he bajado el LinEnum.sh (de **https://github.com/rebootuser/LinEnum/** no de LinEnum.sh que es un troleo), lo he subido a la máquina atacada con un *scp* y me ha dado mucha información pero ninguna que me haya parecido relevante.

- Si que ha sido buena idea lo de buscar todos los ficheros que tengan permisos de lectura/escritura para todos los usuarios.
  ```bash
  find / -type f -perm 777 2> /dev/null
  ```
<img width="872" height="95" alt="image" src="https://github.com/user-attachments/assets/f4d1b1c3-7def-47d4-9648-03de54efeef7" />

- Me bajo los dos ficheros a Kali. Uno parece una lista de más de 3M de claves y la otra es un fichero *ncap*.
 
- Abro el fichero *ncap* y veo que contiene trafico 802.11. No encuentro nada.
<img width="1274" height="408" alt="image" src="https://github.com/user-attachments/assets/885ca866-3846-4b32-b3bc-cddad154f9be" />
  
- Por sugerencia de una página (que también sugería LinEnum y no ha servido de mucho mas que para conocer ese recurso) pruebo a crackear ese tráfico con la lista de claves.
```bash
aircrack-ng -w gold_star.txt wytshadow.cap
```
<img width="576" height="330" alt="image" src="https://github.com/user-attachments/assets/af39faf8-dfa7-45ce-b47c-49cc43bca729" />

- Después de un rato encuentra la clave. Ya tengo la contraseña del usuario **wytshadow**.
<img width="548" height="322" alt="image" src="https://github.com/user-attachments/assets/78c65969-aa6c-413f-a5a2-3eca64219a1a" />

- Hago un *su* con el usuario **wytshadow** e inspecciono su directorio. Lo único que hay es una aplicación que tiene el SUID activado y muestra continuamente un mensaje. No hay por donde meterle mano para conseguir un overflow.
<img width="574" height="298" alt="image" src="https://github.com/user-attachments/assets/694d52da-2f5b-4267-a12a-0bb2bba77918" />

- Si verifico con *sudo -l* qué puede hacer este ususario (cosa que tomo nota que debo hacer con cada usuario) me dice que este usuario puede arrancar el servdor nginx.
<img width="781" height="156" alt="image" src="https://github.com/user-attachments/assets/e146a495-acd2-4ffa-b379-552b595efb53" />

- Pongo en marcha el servidor *nginx*. Veo que ahora también responde por el puerto 8080.
<img width="793" height="230" alt="image" src="https://github.com/user-attachments/assets/c9b850aa-bd51-4224-9af0-77799d3640dd" />

- A partir de la configuración de *nginx* veo que, si no paso como agente el valor **Lynx***, nos va a devolver un 403.
<img width="700" height="482" alt="image" src="https://github.com/user-attachments/assets/b2b34978-8ba3-4796-8adb-9061b7a60f73" />

- Lo verifico cargando la URL con un *curl*. A continuación pruebo a pasar el agente requerido y sí me devuelve contenido: la contraseña del usuario **genphlux**.
<img width="438" height="275" alt="image" src="https://github.com/user-attachments/assets/b9528842-6988-4960-a25c-fa30e1e28d0b" />

- Hago un *su* con el usuario **genphlux** y ahora lo primero que verifico es qué puede hacer como *sudo*. Y veo que puede poner en marcha Apache.
<img width="792" height="127" alt="image" src="https://github.com/user-attachments/assets/03edb810-e4b8-4dec-8de1-896089ca843d" />

- Antes de poner en marcha el servidor Apache, compruebo qué hay en el directorio de este usuario. Veo que hay dos ficheros. El fichero **maleus** contiene una clave privada.
<img width="532" height="338" alt="image" src="https://github.com/user-attachments/assets/a2c1ffad-beba-4e29-9617-572950ea3b2d" />

- Y el fichero xlogin continene una página HTML. Posiblemente sean para el servidor Apache. 
<img width="870" height="243" alt="image" src="https://github.com/user-attachments/assets/e592e8a5-2d8b-4e01-ba94-7f6e60feed2d" />

- Pongo en marcha Apache. Verifico con *nmap* que ahora está escuchando por el puerto 80.
<img width="788" height="254" alt="image" src="https://github.com/user-attachments/assets/a96f67f8-5115-4421-ba27-59d9573d0063" />

- Si intento cargar la *homepage* me da un error de privilegios. Voy a ver si tiene algún detalle parecido al que había con el *nginx*.
<img width="638" height="218" alt="image" src="https://github.com/user-attachments/assets/1aaaaf7b-a4cd-4d29-9e2d-ec5275e000be" />





