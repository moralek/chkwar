import zipfile
import re
from pathlib import Path
import csv
import sys

DEBUG_ENABLED = False  # Cambia a False para ocultar mensajes de depuración
DEBUG = 1
INFO = 2
WARNING = 3
ERROR = 4

def log(nivel, mensaje):
    if nivel == DEBUG and not DEBUG_ENABLED:
        return
    etiquetas = {
        DEBUG: "[DEBUG]",
        INFO: "[INFO]",
        WARNING: "[WARNING]",
        ERROR: "[ERROR]"
    }
    etiqueta = etiquetas.get(nivel, "[LOG]")
    print(f"{etiqueta} {mensaje}")

# Base path
if getattr(sys, 'frozen', False):
    base_path = Path(sys.executable).parent
else:
    base_path = Path(__file__).parent

archivo_ini = base_path / "chkwar.ini"

def normalizar_ruta(path):
    return path.replace('\\', '/')

def parse_valor(valor):
    valor = valor.strip()
    if valor.startswith('"') and valor.endswith('"'):
        return valor[1:-1]
    return valor

zip_folder = base_path / "wars"
csv_file = base_path / "chkwar.csv"
csv_separator = ";"
menos_info = False
archivos_ok = False

bloques = []
bloque_actual = None

#bloque [CONFIG]
with open(archivo_ini, encoding="utf-8") as f:
    in_config = False
    for linea in f:
        linea = linea.strip()
        if linea.upper() == "[CONFIG]":
            in_config = True
            continue
        if in_config and linea.startswith("[") and not linea.upper().startswith("[CONFIG]"):
            break
        if not linea or linea.startswith(";") or linea.startswith("#"):
            continue
        if "=" not in linea or not in_config:
            continue
        clave, valor = map(str.strip, linea.split("=", 1))
        clave = clave.strip().upper()
        log(DEBUG,f"CONFIG: CLAVE={repr(clave)} | valor={repr(valor)}")
        valor = parse_valor(valor)
        if clave == "CARPETA_ZIP":
            ruta = Path(valor)
            zip_folder = ruta if ruta.is_absolute() else base_path / ruta
        elif clave == "ARCHIVO_CSV":
            ruta = Path(valor)
            csv_file = ruta if ruta.is_absolute() else base_path / ruta
        elif clave == "SEPARADOR_CSV":
            csv_separator = valor
        elif clave == "MENOS_INFO":
            menos_info = valor.strip() == "1"
        elif clave in("MOSTRAR_OK","ARCHIVOS_OK"):
            archivos_ok = valor.strip() == "1"

#bloques [CHECKX]          
with open(archivo_ini, encoding="utf-8") as f:
    for linea in f:
        linea = linea.strip()
        if not linea or linea.startswith(";") or linea.startswith("#"):
            continue
        if linea.startswith("[") and linea.endswith("]"):
            seccion = linea[1:-1].strip()
            if seccion.upper().startswith("CHECK") and seccion[5:].isdigit():
                if bloque_actual:
                    bloques.append(bloque_actual)
                bloque_actual = {"FILES": [], "REGLAS": [], "ZIPRAW": "", "SECCION": seccion}
            continue
        if "=" not in linea or bloque_actual is None:
            continue
        clave, valor = map(str.strip, linea.split("=", 1))
        clave = clave.strip().upper()
        valor = parse_valor(valor)
        if clave in {"FILES", "ZIPLST", "ARCHIVOS"}:
            bloque_actual["FILES"].extend([parse_valor(v.strip()) for v in valor.split(",")])
            bloque_actual["ZIPRAW"] = f"{clave}={valor}"
        else:
            if clave.endswith("+") or clave.endswith("-"):
                signo = clave[-1]
                nombre = clave[:-1]
            else:
                signo = "+"
                nombre = clave
            bloque_actual["REGLAS"].append((nombre, valor, signo))
    if bloque_actual:
        bloques.append(bloque_actual)
        
def chkdir(zipf, path):
    ruta = normalizar_ruta(path).rstrip('/')
    return int(any(entry.filename.rstrip('/') == ruta for entry in zipf.infolist()))

def chkfil(zipf, path):
    patron = normalizar_ruta(path)
    patron = patron.replace("**", "___RECURSIVO___")
    patron = re.escape(patron)
    patron = patron.replace("___RECURSIVO___", ".+")
    patron = patron.replace(r"\*", "[^/]*")
    return sum(1 for name in zipf.namelist() if re.fullmatch(patron, name))


def chktxt(zipf, instruccion):
    if ":" not in instruccion:
        return -1
    ruta_archivo, texto = instruccion.split(":", 1)
    ruta = normalizar_ruta(ruta_archivo)
    try:
        with zipf.open(ruta) as f:
            contenido = f.read().decode("utf-8", errors="ignore")
            lineas = contenido.splitlines()
            return sum(line.count(texto) for line in lineas)
    except KeyError:
        return 0

try:
    resultado_csv = []

    for bloque in bloques:
        patrones = bloque["FILES"]
        reglas = bloque["REGLAS"]
        archivos = []
        for patron in patrones:
            archivos.extend(zip_folder.glob(patron))
        archivos = list(dict.fromkeys(archivos))
        
        tipo = "ERROR" if len(archivos) == 0 else "INFO"
        resultado_csv.append((f"[{bloque['SECCION']}]", bloque["ZIPRAW"], len(archivos), tipo))

        for archivo in archivos:
            try:
                with zipfile.ZipFile(archivo, 'r') as zipf:
                    filas = 0
                    for clave, valor, signo in reglas:
                        comando = f"{clave}{signo}={valor}"
                        if clave == "MSGRUN":
                            resultado_csv.append((archivo.name, comando, -1, "INFO"))
                            filas += 1
                            continue
                        if clave == "CHKDIR":
                            cantidad = chkdir(zipf, valor)
                        elif clave == "CHKFIL":
                            cantidad = chkfil(zipf, valor)
                        elif clave == "CHKTXT":
                            cantidad = chktxt(zipf, valor)
                        else:
                            continue
                        if cantidad == -1 or (signo == "+" and cantidad == 0) or (signo == "-" and cantidad > 0):
                            es_error = True
                            tipo = "ERROR"
                        else:
                            es_error = False
                            tipo = "INFO"

                        if not menos_info:
                            log(DEBUG, f"if not menos_info | comando={comando} | signo={signo} | cantidad={cantidad} | menos_info={menos_info}")
                            resultado_csv.append((archivo.name, comando, cantidad, tipo))
                            filas += 1
                        else:
                            if es_error:
                                log(DEBUG, f"cantidad == -1     | comando={comando} | signo={signo} | cantidad={cantidad} | menos_info={menos_info}")
                                resultado_csv.append((archivo.name, comando, cantidad, tipo))
                                filas += 1
                            else:
                                log(DEBUG, f"regla ignorada     | comando={comando} | signo={signo} | cantidad={cantidad} | menos_info={menos_info}")

                    if archivos_ok and filas == 0:
                        resultado_csv.append((archivo.name, "ok", -1, "INFO"))
            except Exception:
                resultado_csv.append((archivo.name, "ERROR: no se pudo abrir el archivo", -1, "ERROR"))

    with open(csv_file, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f, delimiter=csv_separator)
        writer.writerow(["Archivo", "Comando", "Hits", "Tipo"])
        writer.writerows(resultado_csv)

    log(INFO, f"Archivo generado: {csv_file.name}")
    log(DEBUG, f"generado en: {csv_file}")

except Exception as e:
    log(ERROR, f"Error en CHKWAR: {str(e)}")
    sys.exit(1)
