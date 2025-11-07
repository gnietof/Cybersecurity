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

- Pruebo a cargar la URL del servidor Web que me sugiere en el fichero **/y0ur_self** y veo que hay un fichero llamado answers.txt que contiene casi 100000 líneas. Cada una de estas líneas contiene un texto cdificado con Base64.
- Paso esa lista a otro fichero y con un bucle en bash decodifico cada una de las cadenas y las guardo en un fichero.

```bash
while read string; do base64 $string;done < ../Downloads/answer.txt > output.txt
```  

<img width="1225" height="235" alt="image" src="https://github.com/user-attachments/assets/7d354bb9-112a-473a-a649-c19578d7f522" />





- Buscando en ExploitDB encuentro un código en Python que permite explotar una vulnerabilidad de 'Username Enumeration' (https://www.exploit-db.com/exploits/45210). Descargo el código pero necesito instalar en mi equipo varios paquetes. Empiezo por enstalar pip3.

```bash
sudo apt-get update
sudo apt-get install python3-pip

```

Luego instalo los módulos que me hacen falta. Primero unas librerías que le hacen falta a la instalación de paramiko y el soporte de rust. También incluyo OpenSSL para que me lo actualice.

Despues de la instalación de rust es necesario actualizar el entorno.

```bash
sudo apt-get install pkg-config libffi-dev libssl-dev openssl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.bashrc
```
Nota. En Ubuntu 18 me daba problemas las versiones de los paquetes (de OpenSSL por ejemplo que era sólo la 1.1.1). En Ubuntu 24 me obliga a instalar python-env y a crear un entorno antes de poder instalar paramiko.

```bash
sudo apt-get install python3.12-venv
python3 -m venv venv
source venv/bin/activate
```

Finalmente instalo paramiko. Aunque hay que instalar una versión anterior para que no dé problemas.

```bash
pip3 install six setuptools-rust
pip3 install paramiko #==2.4.1 Si instalo una versión anterior, paramiko choca con Python 3.12
```

Despues de prueba y error parece que tengo todos los prerrequisitos necesarios. Y parece que se instala ... a pesar del *segmentation fault* que aparece al final.
<img width="995" height="98" alt="image" src="https://github.com/user-attachments/assets/026e14c1-f2ff-4105-be54-1215934d597a" />



