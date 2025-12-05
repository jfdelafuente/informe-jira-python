# 🔧 Solución de Problemas de Instalación

Guía para resolver problemas comunes al instalar dependencias del proyecto.

---

## ❌ Problema: "pip install -r requirements.txt" falla con pandas

### Síntomas

```
ERROR: Failed building wheel for pandas
ERROR: Could not build wheels for pandas
```

o

```
error: Microsoft Visual C++ 14.0 or greater is required
```

---

## ✅ Soluciones (en orden de más rápida a más compleja)

### Solución 1: Usar requirements-compatible.txt (⭐ RECOMENDADO)

He creado un archivo alternativo con versiones más compatibles:

```bash
# En lugar de:
pip install -r requirements.txt

# Usa:
pip install -r requirements-compatible.txt
```

Este archivo usa versiones de pandas que ya vienen precompiladas para Windows.

---

### Solución 2: Instalar pandas precompilado primero

```bash
# 1. Actualizar pip
python -m pip install --upgrade pip

# 2. Instalar wheel
pip install wheel

# 3. Instalar pandas específicamente (versión precompilada)
pip install pandas==2.0.3

# 4. Luego instalar el resto
pip install requests python-dotenv openpyxl
```

---

### Solución 3: Usar versiones específicas sin compilar

Edita `requirements.txt` temporalmente:

```bash
# Abre requirements.txt y cambia:
pandas>=2.1.0

# Por:
pandas==2.0.3
```

Luego:
```bash
pip install -r requirements.txt
```

---

### Solución 4: Instalar Microsoft C++ Build Tools (Windows)

Si las anteriores no funcionan, necesitas las herramientas de compilación:

**Opción A - Build Tools (Ligero, ~1 GB):**

1. Descarga: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Ejecuta el instalador
3. Selecciona: "Herramientas de compilación de C++"
4. Espera la instalación (puede tardar 15-30 min)
5. Reinicia la terminal
6. Ejecuta: `pip install -r requirements.txt`

**Opción B - Visual Studio Community (Completo, ~7 GB):**

1. Descarga: https://visualstudio.microsoft.com/downloads/
2. Instala Visual Studio Community
3. Durante instalación, selecciona "Desarrollo de escritorio con C++"
4. Reinicia después de instalar
5. Ejecuta: `pip install -r requirements.txt`

---

### Solución 5: Usar Anaconda/Miniconda (Alternativa completa)

Si nada funciona, usa Anaconda que viene con pandas preinstalado:

```bash
# 1. Descarga Miniconda
# https://docs.conda.io/en/latest/miniconda.html

# 2. Crea entorno
conda create -n jira-env python=3.11

# 3. Activa entorno
conda activate jira-env

# 4. Instala dependencias
conda install pandas requests python-dotenv openpyxl

# 5. Si algo no está en conda, usa pip
pip install python-dotenv  # por si conda no lo tiene
```

---

## 🔍 Diagnóstico: ¿Cuál es mi problema?

Ejecuta estos comandos para diagnosticar:

```bash
# 1. Versión de Python
python --version

# 2. Versión de pip
pip --version

# 3. ¿Tienes compilador C++?
# Windows:
where cl

# Si no encuentra "cl.exe", necesitas Build Tools
```

---

## 📋 Pasos Recomendados por Sistema

### Windows 10/11

```powershell
# Método más rápido (95% de éxito)
python -m pip install --upgrade pip
pip install -r requirements-compatible.txt

# Si falla, instalar uno por uno
pip install requests
pip install python-dotenv
pip install openpyxl
pip install pandas==2.0.3
```

### Linux (Ubuntu/Debian)

```bash
# Instalar dependencias del sistema primero
sudo apt-get update
sudo apt-get install python3-dev python3-pip

# Luego instalar paquetes Python
pip install -r requirements.txt

# Si falla pandas
pip install --no-cache-dir pandas
```

### macOS

```bash
# Actualizar pip
python3 -m pip install --upgrade pip

# Instalar dependencias
pip3 install -r requirements.txt

# Si falla, usar homebrew para instalar pandas
brew install python@3.11
pip3 install pandas
```

---

## 🎯 Solución Paso a Paso (Copy-Paste)

### Para Windows (PowerShell)

```powershell
# 1. Ir al directorio del proyecto
cd "c:\My Program Files\workspace-python\sonar_jira_gitlab_api\informe-jira-python"

# 2. Activar entorno virtual (si existe)
.\venv\Scripts\activate

# 3. Actualizar herramientas
python -m pip install --upgrade pip setuptools wheel

# 4. Instalar con archivo compatible
pip install -r requirements-compatible.txt

# 5. Verificar instalación
python -c "import pandas; print(f'Pandas {pandas.__version__} instalado OK')"
```

### Para Linux/Mac (Bash)

```bash
# 1. Ir al directorio del proyecto
cd /ruta/a/informe-jira-python

# 2. Activar entorno virtual (si existe)
source venv/bin/activate

# 3. Actualizar herramientas
python -m pip install --upgrade pip setuptools wheel

# 4. Instalar dependencias
pip install -r requirements-compatible.txt

# 5. Verificar instalación
python -c "import pandas; print(f'Pandas {pandas.__version__} instalado OK')"
```

---

## ⚡ Instalación Mínima (Solo lo Esencial)

Si solo quieres que funcione rápido:

```bash
pip install requests==2.31.0
pip install pandas==2.0.3
pip install python-dotenv==1.0.0
pip install openpyxl==3.1.2
```

Luego verifica:
```bash
python -c "import requests, pandas, dotenv, openpyxl; print('Todo OK')"
```

---

## 🔴 Errores Específicos y Soluciones

### Error: "No module named 'numpy'"

```bash
pip install numpy==1.24.3
pip install pandas==2.0.3
```

### Error: "externally-managed-environment"

En Python 3.11+ en Linux:

```bash
# Opción 1: Usar entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Opción 2: Instalar con --break-system-packages (no recomendado)
pip install --break-system-packages -r requirements.txt
```

### Error: "SSLError" o problemas de certificados

```bash
# Instalar con --trusted-host
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pandas
```

### Error: Timeout al descargar

```bash
# Aumentar timeout
pip install --timeout=120 -r requirements.txt

# O usar mirror alternativo
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas
```

---

## ✅ Verificación Final

Después de instalar, verifica que todo funciona:

```bash
# Opción 1: Script de validación
python validar_entorno.py

# Opción 2: Verificación manual
python -c "
import requests
import pandas
import dotenv
import openpyxl
print('✓ requests:', requests.__version__)
print('✓ pandas:', pandas.__version__)
print('✓ python-dotenv: OK')
print('✓ openpyxl:', openpyxl.__version__)
print('\nTodas las dependencias instaladas correctamente!')
"
```

---

## 📦 Alternativa: Archivo Wheels Precompilados

Si nada funciona, descarga wheels precompilados:

1. Ve a: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pandas
2. Descarga el wheel para tu versión:
   - Python 3.11: `pandas‑2.0.3‑cp311‑cp311‑win_amd64.whl`
3. Instala localmente:
   ```bash
   pip install ruta/al/archivo.whl
   ```

---

## 🆘 Si Nada Funciona

### Plan B: Usar Python 3.10

Python 3.10 tiene mejor compatibilidad con pandas precompilados:

```bash
# 1. Desinstalar Python 3.11
# 2. Instalar Python 3.10 desde python.org
# 3. Crear nuevo entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 4. Instalar dependencias
pip install -r requirements.txt
```

### Plan C: Usar Docker

Si tienes Docker instalado:

```bash
# Crear Dockerfile
cat > Dockerfile << EOF
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "JiraOrange/jira_bugs_to_json.py"]
EOF

# Construir imagen
docker build -t jira-etl .

# Ejecutar
docker run -v $(pwd)/in:/app/in -v $(pwd)/out:/app/out jira-etl
```

---

## 📊 Compatibilidad de Versiones

| Python | pandas | numpy | Recomendación |
|--------|--------|-------|---------------|
| 3.11   | 2.0.x  | 1.24.x| ⚠️ Puede requerir compilador |
| 3.10   | 2.0.x  | 1.23.x| ✅ Mejor compatibilidad |
| 3.9    | 1.5.x  | 1.21.x| ✅ Muy estable |

---

## 🎓 Prevención para el Futuro

Para evitar estos problemas:

1. **Usa siempre entorno virtual:**
   ```bash
   python -m venv venv
   ```

2. **Especifica versiones exactas** (no >=):
   ```
   pandas==2.0.3  # Bueno
   pandas>=2.1.0  # Puede causar problemas
   ```

3. **Actualiza pip primero:**
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Considera usar Poetry o Pipenv** para gestión de dependencias

---

## 📝 Comando Todo-en-Uno

Copia y pega este comando que prueba varias soluciones:

```bash
# Windows PowerShell
python -m pip install --upgrade pip setuptools wheel && (pip install -r requirements-compatible.txt || pip install requests pandas==2.0.3 python-dotenv openpyxl) && python -c "import pandas; print('Pandas OK')"

# Linux/Mac Bash
python -m pip install --upgrade pip setuptools wheel && (pip install -r requirements-compatible.txt || pip install requests pandas==2.0.3 python-dotenv openpyxl) && python -c "import pandas; print('Pandas OK')"
```

---

## 💬 Resumen de Soluciones

| Problema | Solución Rápida |
|----------|-----------------|
| pandas no compila | `pip install -r requirements-compatible.txt` |
| Falta compilador C++ | Instalar Build Tools o usar pandas==2.0.3 |
| Error de numpy | `pip install numpy` primero |
| Timeout | `pip install --timeout=120` |
| Sin permisos (Linux) | Usar entorno virtual |

---

## 🔗 Enlaces Útiles

- [pandas Installation](https://pandas.pydata.org/docs/getting_started/install.html)
- [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- [Precompiled Wheels](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

---

**Última actualización:** 2025-12-02

Si ninguna solución funciona, por favor:
1. Ejecuta `python validar_entorno.py --verbose`
2. Copia el error completo
3. Indica tu sistema operativo y versión de Python
