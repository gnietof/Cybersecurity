# VulnHub

## Troll1
- Hago un port scan con NMap (nmap -sV -O -n 192168.161.0/24) para ver qué equipos y que puertos/servicios tienen levantados. La máquina Troll1 tiene dos adaptadores y espero encontrar dos IP respondiendo.
- Encuentro efectivamente dos IP. En una de ellas veo que están levantados los puertos 21 (VSFtpd 2.0.8, vulnerable) y 22 (OpenSSH 5.9p1, vulnerable).
<img width="801" height="255" alt="image" src="https://github.com/user-attachments/assets/17233f55-3631-426e-bf9a-5794d0a45dd4" />
- Buscando en ExploitDB encuentro un código en Python que permite explotar una vulnerabilidad de 'Username Enumeration'. Descargo el código pero necesito instalar en mi equipo varios paquetes. Empiezo por enstalar pip3.

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

Finalmente instalo paramiko.

```bash
pip3 install setuptools-rust
pip3 install paramiko
```

Despues de prueba y error parece que tengo todos los prerrequisitos necesarios. Y parece que se instala ... a pesar del *segmentation fault* que aparece al final.
<img width="995" height="98" alt="image" src="https://github.com/user-attachments/assets/026e14c1-f2ff-4105-be54-1215934d597a" />



