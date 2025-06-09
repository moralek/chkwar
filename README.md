(Nota: Readme creado por ChatGPT mientra tanto, (hasta que tenga un tiempo de hacerlo bien):

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
