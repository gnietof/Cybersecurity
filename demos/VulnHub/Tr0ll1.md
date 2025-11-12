# VulnHub

## Tr0ll1
- Primero hago el barrido con nmap para averiguar la IP de la máquina virtual y saber qué puertos tiene abiertos. Veo que tiene abierto el ftp, el ssh y el http.
<img width="368" height="144" alt="image" src="https://github.com/user-attachments/assets/96aeaed6-8ec3-4a22-9c65-a70f418cfabb" />

- Y luego hago una busqueda más dirigida.
<img width="784" height="256" alt="image" src="https://github.com/user-attachments/assets/d8e9b5a2-6ab7-47db-ae73-f9670696d433" />


- Con Metasploit hago un barrido de usuario a ssh. No sé si luego me servirá para algo.
<img width="603" height="463" alt="image" src="https://github.com/user-attachments/assets/27c36ae8-4cd4-46f6-8b56-3cf87e7bd446" />

- Tiene abierto el puerto HTTP. Cargo la *homepage*. Veo una imagen sin más. No hay nada en el contenido de la página.
<img width="577" height="487" alt="image" src="https://github.com/user-attachments/assets/854a0580-8e2b-4280-94f2-40c752cabc82" />

- Intento cargar la página **/robots.txt** a ver si encuentro alguna página escondida. Y veo que existe la página **/secret**.
<img width="576" height="361" alt="image" src="https://github.com/user-attachments/assets/23ee1cff-9064-4f73-a515-9b6a7403fa6b" />

- Cargo la página **/secret** pero no hay nada.
<img width="762" height="650" alt="image" src="https://github.com/user-attachments/assets/c0760520-81d8-461a-95bf-08c1db08c15e" />

- Intento conectarme por FTP y me dice que sólo puedo conectarme como anónimo. Así que me conecto como anónimo sin propoprcionar ninguna contraseña.
<img width="319" height="237" alt="image" src="https://github.com/user-attachments/assets/45400839-5559-4811-b928-972225dc0983" />

- Saco un listado y veo que hay un fichero de captura de tráfico. Me lo descargo.
<img width="1256" height="210" alt="image" src="https://github.com/user-attachments/assets/ad42b0e7-2713-4a3a-a4bc-a382d3f42f8b" />

- Me desconecto y abro el fichero con WireShark para analizarlo. Veo que en los paquetes de datos menciona algo de un directorio.
<img width="1275" height="726" alt="image" src="https://github.com/user-attachments/assets/54155833-5142-404c-9917-ec37b2a76989" />

- Pruebo a cargar ese directorio **sup3rs3cr3tdirlol** en el navegador y ahora sí. Pincho en el enlace del fichero y me lo descarga.
<img width="567" height="323" alt="image" src="https://github.com/user-attachments/assets/ea343afc-b0b2-4cda-8174-304d7aec92f2" />

- He volcado el fichero y veo que es un ejecutable. Doy privilegios de ejecución al fichero y lo lanzo.
<img width="310" height="116" alt="image" src="https://github.com/user-attachments/assets/3ea2cea9-4984-4682-b646-b2357c39f0c8" />

- Me dice que encuentre la dirección **0x0856BF** paras continuar. Voy a probar a ver si esta también es un directorio dentro de la web. Una vez más he tenido suerte. 
<img width="632" height="366" alt="image" src="https://github.com/user-attachments/assets/57830a94-fb10-42c2-ab54-f288f111f056" />

- Siguiendo el primer enlace llego a un fichero con una lista de lo que parecen usuarios. Me copio la lista.
<img width="698" height="254" alt="image" src="https://github.com/user-attachments/assets/dc98e4be-15e1-4727-9975-474d1a9c2261" />

- Y siguiendo el segundo llegamos a un fichero que parece que tiene una contraseña.
<img width="833" height="137" alt="image" src="https://github.com/user-attachments/assets/5106c272-0ad3-4019-8517-4602affd1c1f" />

- Utilizo **hydra** para probar todos los usuarios con esa contraseña contra ssh. Pero no me encuentra nada.
<img width="911" height="196" alt="image" src="https://github.com/user-attachments/assets/627d62eb-b55c-4cbd-8654-72b95ba182e5" />

- Se me ocurre que quizá la contraseña no es la que está dentro del fichero sino el propio Pass.txt. Vuelvo a probar y veo que ahora sí esa es la contraseña del usuario **overflow**.
<img width="908" height="207" alt="image" src="https://github.com/user-attachments/assets/4b56ecf5-fc35-43d2-b600-1a2df484c539" />

- Me conecto con esos credenciales mediante *ssh*.
<img width="627" height="420" alt="image" src="https://github.com/user-attachments/assets/dffb860a-271e-4c61-9808-2e217abdc18c" />

- Verifico si puedo hacer algo con *sudo*. Nada.
<img width="396" height="87" alt="image" src="https://github.com/user-attachments/assets/850cdf88-da6d-4e54-8808-2408c934ca3c" />

- Después de estar un rato enredando y no ver nada más que que el usuario overflow no tiene directorio home, me echa y cierra la sesión. 
<img width="442" height="136" alt="image" src="https://github.com/user-attachments/assets/c3938284-9817-438c-b9ef-6d28f190f14a" />

- Así que debe haber algún proceso que se ejecute perióicamente con un *cron*. Lo busco. Y veo que efectivamente se ejecuta el *script* cleaner.py cada dos minutos. 
<img width="339" height="106" alt="image" src="https://github.com/user-attachments/assets/013bd68d-b932-492d-84fc-15923e692837" />

- Veo que ese fichero cleaner.py es editable.
<img width="449" height="234" alt="image" src="https://github.com/user-attachments/assets/2ba152c1-3398-4fa1-b9f6-1df06c0ee1c5" />

- Me bajo un reverse shell de https://ironhackers.es/en/herramientas/reverse-shell-cheat-sheet/ y lo incluyo en en el script de Python. Modifico la IP para que apunte a mi maquina atacante. He formateado el Python aunque no sería necesario. 
<img width="566" height="275" alt="image" src="https://github.com/user-attachments/assets/e9d6495b-068c-4964-a975-230159284262" />

- En la máquina atacante arrancamos un netcat y a esperar. Cuando el script se ejecuta se conecta a nuestra máquina y ese script se ejecuta como root. Ahora solo tengo que buscar el fichero con el token.
<img width="456" height="221" alt="image" src="https://github.com/user-attachments/assets/fa929bbd-1cee-4cf4-b330-430cce7503fc" />


