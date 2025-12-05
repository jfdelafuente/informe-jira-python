# 🚀 Inicio Rápido - Informe Jira Python

Guía rápida para poner en marcha el proyecto en **menos de 5 minutos**.

---

## ⚡ Setup Rápido (Copiar y Pegar)

### Opción 1: Windows

```powershell
# 1. Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate

# 2. Instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Configurar credenciales
copy .env.example .env
notepad .env
# → Edita y guarda: USUARIO=tu_usuario y PASS=tu_password

# 4. Validar entorno
python validar_entorno.py

# 5. Preparar archivo de entrada
notepad in\incidencias_in.csv
# → Agrega tus incidencias (ver ejemplo abajo)

# 6. ¡Ejecutar!
python JiraOrange\jira_bugs_to_json.py
```

### Opción 2: Linux/Mac

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 3. Configurar credenciales
cp .env.example .env
nano .env
# → Edita: USUARIO=tu_usuario y PASS=tu_password
# → Guarda: Ctrl+O, Enter, Ctrl+X

# 4. Validar entorno
python validar_entorno.py

# 5. Preparar archivo de entrada
nano in/incidencias_in.csv
# → Agrega tus incidencias (ver ejemplo abajo)

# 6. ¡Ejecutar!
python JiraOrange/jira_bugs_to_json.py
```

---

## 📋 Paso a Paso Detallado

### Paso 1: Verificar Python

Asegúrate de tener Python 3.7 o superior:

```bash
python --version
# Debe mostrar: Python 3.7.x o superior
```

Si no lo tienes, descárgalo desde [python.org](https://www.python.org/downloads/)

---

### Paso 2: Clonar/Descargar el Proyecto

Si aún no tienes el proyecto:

```bash
# Opción A: Con Git
git clone <url-del-repositorio>
cd informe-jira-python

# Opción B: Descarga manual
# Descarga el ZIP, extrae y entra a la carpeta
cd informe-jira-python
```

---

### Paso 3: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Deberías ver (venv) al inicio de la línea de comandos
```

---

### Paso 4: Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt

# Verás algo como:
# Installing collected packages: requests, pandas, python-dotenv, openpyxl
# Successfully installed...
```

---

### Paso 5: Configurar Credenciales

**Crear archivo .env:**

```bash
# Windows:
copy .env.example .env

# Linux/Mac:
cp .env.example .env
```

**Editar con tus credenciales:**

```bash
# Windows:
notepad .env

# Linux/Mac:
nano .env
# o
vim .env
```

**Contenido del .env:**

```env
USUARIO=tu_usuario_jira
PASS=tu_password_jira
```

⚠️ **IMPORTANTE:**
- Reemplaza `tu_usuario_jira` con tu usuario real
- Reemplaza `tu_password_jira` con tu contraseña real
- NO compartas este archivo (ya está en .gitignore)

---

### Paso 6: Validar Entorno

```bash
python validar_entorno.py
```

**Si todo está OK, verás:**

```
✓ ENTORNO VÁLIDO
El proyecto está listo para ejecutarse.
```

**Si hay errores:**
- Lee los mensajes de error
- Sigue las soluciones sugeridas
- Vuelve a ejecutar `python validar_entorno.py`

---

### Paso 7: Preparar Archivo de Entrada

**Crear archivo de incidencias:**

```bash
# El directorio 'in/' ya existe (se crea automáticamente)
# Crea el archivo CSV:

# Windows:
notepad in\incidencias_in.csv

# Linux/Mac:
nano in/incidencias_in.csv
```

**Formato del archivo:**

```csv
Incidencia
INC000000012345
INC000000067890
INC000000098765
```

**Ejemplo real:**

```csv
Incidencia
INC000000012345
INC000000012346
INC000000012347
```

✓ Primera línea: `Incidencia` (cabecera)
✓ Siguientes líneas: Números de incidencia

---

### Paso 8: Ejecutar Proceso Completo

El proyecto tiene 4 scripts principales que se ejecutan en orden:

#### 8.1 Extraer Bugs de Jira

```bash
python JiraOrange/jira_bugs_to_json.py
```

**Qué hace:**
- Lee `in/incidencias_in.csv`
- Consulta Jira por cada incidencia
- Guarda JSONs en `JSON/BUGS/`

**Salida esperada:**
```
Inicio consulta incidencias ...
Leyendo ... incidencias_in.csv
Data Quality OK
Fin. Procesadas 3 incidencias
COPY duration: 12.34 seconds
```

---

#### 8.2 Extraer Deliveries de Jira (Opcional)

```bash
python JiraOrange/jira_delivs_to_json.py
```

**Qué hace:**
- Consulta deliveries asociadas a bugs
- Guarda JSONs en `JSON/DELIVS/`

**Nota:** Este script tiene bugs hardcodeados. Edítalo si necesitas otros.

---

#### 8.3 Procesar ETL de Bugs

```bash
python JiraOrange/jira_bugs_etl.py
```

**Qué hace:**
- Lee JSONs de `JSON/BUGS/`
- Transforma y limpia datos
- Genera `salida_bugs.csv`

**Salida esperada:**
```
Extract phase Started
Extract phase Ended
Transform phase Started
Transform phase Ended
Load phase Started
Load phase Ended
Proceso completado. Duración: 2.45 seconds
```

**Archivo generado:** `salida_bugs.csv`

---

#### 8.4 Procesar ETL de Deliveries (Opcional)

```bash
python JiraOrange/jira_delivs_etl.py
```

**Qué hace:**
- Lee JSONs de `JSON/DELIVS/`
- Transforma datos
- Genera `salida_delivs.csv`

**Archivo generado:** `salida_delivs.csv`

---

## 📁 Estructura de Archivos Generados

Después de ejecutar todo, tendrás:

```
informe-jira-python/
├── in/
│   └── incidencias_in.csv          ← TÚ LO CREAS
├── JSON/
│   ├── BUGS/
│   │   ├── INC000000012345_bugs_new.json
│   │   ├── INC000000012346_bugs_new.json
│   │   └── ...
│   └── DELIVS/
│       ├── DELIV-12345_delivs_news.json
│       └── ...
├── salida_bugs.csv                 ← RESULTADO FINAL
├── salida_delivs.csv               ← RESULTADO FINAL
└── jira_bugs_logfile.txt           ← LOG
```

---

## ✅ Checklist de Verificación

Marca cada paso conforme lo completes:

- [ ] Python 3.7+ instalado
- [ ] Proyecto descargado/clonado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` creado con credenciales
- [ ] Validación exitosa (`python validar_entorno.py`)
- [ ] Archivo `in/incidencias_in.csv` creado con incidencias
- [ ] Script `jira_bugs_to_json.py` ejecutado sin errores
- [ ] Script `jira_bugs_etl.py` ejecutado sin errores
- [ ] Archivo `salida_bugs.csv` generado correctamente

---

## 🔧 Solución de Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'requests'"

**Causa:** No instalaste las dependencias.

**Solución:**
```bash
pip install -r requirements.txt
```

---

### Error: "Credenciales de Jira no configuradas"

**Causa:** Archivo `.env` no existe o está vacío.

**Solución:**
```bash
# Crear .env desde plantilla
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# Editar con tus credenciales
nano .env  # o notepad .env en Windows
```

---

### Error: "No se encontró el archivo incidencias_in.csv"

**Causa:** No creaste el archivo de entrada.

**Solución:**
```bash
# Crear archivo
nano in/incidencias_in.csv

# Agregar contenido:
Incidencia
INC000000012345
```

---

### Error: "Connection refused" al conectar a Jira

**Causas posibles:**
1. Sin conexión a internet
2. VPN desconectada (si tu Jira requiere VPN)
3. Credenciales incorrectas
4. Firewall bloqueando

**Solución:**
```bash
# Verificar conectividad
ping jira.si.orange.es

# Verificar credenciales en navegador
# Intenta loguearte en https://jira.si.orange.es

# Verificar que .env tenga las credenciales correctas
cat .env  # Linux/Mac
type .env  # Windows
```

---

### Error: "Permission denied" al escribir archivos

**Causa:** Sin permisos de escritura en directorios.

**Solución:**
```bash
# Linux/Mac:
chmod -R 755 .

# Windows:
# Ejecutar cmd como administrador
icacls . /grant Users:F /T
```

---

### El script se queda "colgado"

**Causa:** Consulta a Jira muy lenta o timeout.

**Solución:**
- Espera un poco más (puede tardar con muchas incidencias)
- Verifica tu conexión a internet
- Reduce el número de incidencias en el CSV para probar

---

## 🎯 Flujo de Trabajo Típico

### Primera Vez (Setup)

```bash
1. python -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt
3. cp .env.example .env && nano .env
4. python validar_entorno.py
```

### Cada Ejecución

```bash
# Activar entorno (si no está activo)
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Actualizar archivo de entrada
nano in/incidencias_in.csv

# Ejecutar proceso
python JiraOrange/jira_bugs_to_json.py
python JiraOrange/jira_bugs_etl.py

# Revisar resultados
cat salida_bugs.csv  # o abrirlo en Excel
```

---

## 📊 Abrir Resultados

### En Excel/LibreOffice

```bash
# Los archivos CSV se pueden abrir directamente
# Busca: salida_bugs.csv y salida_delivs.csv
```

**IMPORTANTE:** Los CSV usan `;` como separador.

En Excel:
1. Abrir Excel
2. Datos → Desde texto/CSV
3. Seleccionar `salida_bugs.csv`
4. Cambiar delimitador a `;` (punto y coma)
5. Cargar

### En Python/Pandas

```python
import pandas as pd

# Leer resultados
df = pd.read_csv('salida_bugs.csv', sep=';')
print(df.head())

# Analizar
print(f"Total de bugs: {len(df)}")
print(df['Status'].value_counts())
```

---

## 🔄 Actualizar el Proyecto

Si descargas una nueva versión:

```bash
# Actualizar código
git pull  # Si usas Git

# Reinstalar dependencias (por si hay nuevas)
pip install -r requirements.txt

# Validar que todo sigue OK
python validar_entorno.py
```

---

## 📚 Documentación Adicional

- **[README.md](README.md)** - Documentación completa del proyecto
- **[GUIA_VALIDACION.md](GUIA_VALIDACION.md)** - Guía detallada del script de validación
- **[MEJORAS_IMPLEMENTADAS.md](MEJORAS_IMPLEMENTADAS.md)** - Historial de mejoras
- **[MEJORAS_FUTURAS.md](MEJORAS_FUTURAS.md)** - Roadmap de mejoras planeadas

---

## 💡 Consejos

1. **Mantén el entorno virtual activo** durante toda la sesión de trabajo
2. **Valida con pocas incidencias primero** para probar que funciona
3. **Revisa los logs** si algo falla (`jira_bugs_logfile.txt`)
4. **Haz backup** de tus archivos `.env` y CSVs importantes
5. **Usa `--skip-jira`** en validación si estás offline

---

## 🆘 Ayuda

Si después de seguir esta guía sigues teniendo problemas:

1. **Ejecuta validación detallada:**
   ```bash
   python validar_entorno.py --verbose
   ```

2. **Revisa los logs:**
   ```bash
   cat jira_bugs_logfile.txt  # Linux/Mac
   type jira_bugs_logfile.txt  # Windows
   ```

3. **Verifica versiones:**
   ```bash
   python --version
   pip list
   ```

4. **Consulta la documentación completa** en [README.md](README.md)

---

## ⚡ Comandos de Referencia Rápida

```bash
# Activar entorno
source venv/bin/activate              # Linux/Mac
venv\Scripts\activate                 # Windows

# Validar entorno
python validar_entorno.py

# Extraer bugs
python JiraOrange/jira_bugs_to_json.py

# Extraer deliveries
python JiraOrange/jira_delivs_to_json.py

# ETL bugs
python JiraOrange/jira_bugs_etl.py

# ETL deliveries
python JiraOrange/jira_delivs_etl.py

# Ver logs
tail -f jira_bugs_logfile.txt         # Linux/Mac
Get-Content jira_bugs_logfile.txt -Wait  # Windows PowerShell

# Desactivar entorno
deactivate
```

---

**¡Listo!** Ahora deberías tener el proyecto funcionando. 🎉

Si encuentras algún error, consulta la sección de **Solución de Problemas** o revisa la **[Guía de Validación](GUIA_VALIDACION.md)**.

---

**Última actualización:** 2025-12-02
**Versión:** 1.0
**Tiempo estimado de setup:** 5-10 minutos
