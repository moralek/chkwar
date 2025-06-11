(Nota: Readme creado por ChatGPT mientra tanto, (hasta que tenga un tiempo de hacerlo bien):

- Para que funcione el run.bat debe estar Docker Desktop corriendo

Ruta(orden al azar)
- `pendiente` ordenar el caos de esta ruta, :(
- `ok` Agregar una columna que indique claramente si la fila es INFO o ERROR , 
- `ok` Reordenar las carpetas (eliminar "compartido"), todo en una carpeta bat y script, solo una carpeta adicional para los wars, 
- `ok` Cambiar ZIPLST a FILES, 
- `parcial` Reemplazar MENOS_INFO por un tipo mas claro, algo como "CHKFIL_OK, CHKDIR_OK, CHKTXT_OK" permitiendo ocultar los ok por tipo, mas ordenado. 
- `pendiente` Casos de uso de generación SIGAS, crear el chkwar.ini SIGAS, 
- `pendiente` Revisar si existe un Docker con modulo excel para python para mejorar la ejecucion( agregar autofit, fuente bold, colores en el documento) para evitar build con Dockerfile, 
- `pendiente` Indicadores de mostrar/ocultar para tipos INFO, ERROR, 
- `ok` Etiqueta DEBUG_ENABLED en el .py para revisar el script, 
- `pendiente` Mejora logs cuando DEBUG_ENABLED en py, 
- `pendiente` Crear el readme.md, 
- `pendiente` Testing inicial full, 
- `pendiente` Ver compilación en un exe pero que no detecte el antivirus como falso positivo, 
- `pendiente` Agregar "+ / -" a FILES, para mostrar los que cumplen o aquellos que "no cumplen" con la condicion/patron,
- `pendiente` ver la posibilidad de CLRDIR y DELFIL ( o posible recomprimir y R/W) , 

# chkwar

`chkwar` es una herramienta en Python para inspeccionar archivos `.war` (o `.zip`) de forma automatizada, aplicando reglas definidas en un archivo de configuración `.ini`. Permite verificar la presencia o ausencia de archivos, carpetas y contenidos según patrones personalizables.

---

## 🚀 ¿Para qué sirve?

`chkwar` permite realizar revisiones automatizadas de artefactos `.war`, útiles para pipelines CI/CD, validaciones de entrega o aseguramiento de calidad en entornos Java EE / Jakarta EE.

---

## ⚙️ Requisitos

- Python 3.6 o superior
- Librerías estándar (`re`, `zipfile`, `configparser`, etc.)

---

## 📁 Estructura esperada

- `chkwar.py` — Script principal
- `chkwar.ini` — Archivo con reglas
- Carpeta `wars/` — Ubicación de archivos `.war` a analizar

---

## 🧩 Formato del archivo `chkwar.ini`

```ini
[CHECK1]
CHKDIR+ = WEB-INF/classes/**
CHKFIL- = **/*.bak
CHKTXT+ = /META-INF/MANIFEST.MF:Implementation-Version
```

- `CHKDIR+` valida que exista algún directorio coincidente.
- `CHKFIL-` valida que **no** exista ningún archivo que coincida.
- `CHKTXT+` valida que exista una línea con el texto indicado dentro del archivo especificado.

---

## 🖥️ Ejecución

```bash
python chkwar.py
```

El script procesará todos los `.war` ubicados en la carpeta `wars/` y aplicará las reglas del archivo `chkwar.ini`.

---


## 🧑‍💻 [Autor](https://github.com/moralek)

---

## 🪪 Licencia

MIT License
