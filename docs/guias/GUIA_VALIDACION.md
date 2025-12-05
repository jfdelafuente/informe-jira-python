# Guía del Script de Validación

## ¿Qué es validar_entorno.py?

Es un script de diagnóstico que verifica que tu entorno esté correctamente configurado antes de ejecutar el proyecto. **Ejecutarlo es opcional pero altamente recomendado** antes de la primera ejecución o después de cambios importantes.

---

## Uso Básico

### Validación Completa

```bash
python validar_entorno.py
```

Verifica todos los componentes del sistema.

### Con Información Detallada

```bash
python validar_entorno.py --verbose
```

Muestra información adicional sobre cada componente verificado.

### Sin Probar Conexión a Jira

```bash
python validar_entorno.py --skip-jira
```

Útil si no tienes conectividad en el momento pero quieres verificar el resto.

---

## ¿Qué Verifica?

### 1. ✓ Versión de Python

Verifica que uses **Python 3.7 o superior**.

**Salida esperada:**
```
✓ Versión de Python                           [OK]
  → Python 3.11.0
```

**Si falla:**
```
✗ Versión de Python                           [ERROR]
  → Python 3.6.0 - Se requiere Python 3.7 o superior
```

**Solución:** Actualiza Python desde [python.org](https://www.python.org/downloads/)

---

### 2. ✓ Librerías Instaladas

Verifica que todas las dependencias estén instaladas:
- requests
- pandas
- python-dotenv
- openpyxl

**Salida esperada:**
```
✓ Todas las librerías instaladas                [OK]
  → 4 librerías encontradas
```

**Si falla:**
```
✗ Librerías requeridas                          [ERROR]
  → Faltan 2 librerías
  • pandas
  • openpyxl

  Solución: pip install -r requirements.txt
```

**Solución:**
```bash
pip install -r requirements.txt
```

---

### 3. ✓ Variables de Entorno

Verifica que el archivo `.env` exista y contenga:
- USUARIO (o JIRA_USER)
- PASS (o PASSWORD / JIRA_PASSWORD)

**Salida esperada:**
```
✓ USUARIO/JIRA_USER                             [OK]
  → Configurado (jde***)
✓ PASS/PASSWORD                                 [OK]
  → Configurado (***)
```

**Si falla:**
```
✗ USUARIO/JIRA_USER                             [ERROR]
  → NO CONFIGURADO
✗ PASS/PASSWORD                                 [ERROR]
  → NO CONFIGURADO

  Solución:
  1. Copia .env.example a .env
  2. Edita .env con tus credenciales de Jira
```

**Solución:**
```bash
# En Linux/Mac
cp .env.example .env

# En Windows
copy .env.example .env

# Luego editar .env con tus credenciales
```

---

### 4. ✓ Estructura de Directorios

Verifica que existan todos los directorios necesarios:
- JiraOrange/ y subdirectorios
- in/
- out/
- JSON/BUGS/
- JSON/DELIVS/

**Salida esperada:**
```
✓ Estructura de directorios                     [OK]
  → 9 directorios OK
```

**Si falla:**
```
⚠ Estructura de directorios                     [ADVERTENCIA]
  → Faltan 3 directorios
  • in/
  • JSON/BUGS/
  • JSON/DELIVS/
```

**Solución:** Los directorios se crean automáticamente al importar `configD.py`:
```bash
python -c "import JiraOrange.configD"
```

---

### 5. ✓ Archivos de Código

Verifica que existan todos los módulos Python necesarios.

**Salida esperada:**
```
✓ Archivos de código                            [OK]
  → 10 archivos encontrados
```

**Si falla:**
```
✗ Archivos de código                            [ERROR]
  → Faltan 2 archivos
  • JiraOrange/api/JiraAPIHandler.py
  • JiraOrange/etl/extract.py
```

**Solución:** Restaura los archivos desde el repositorio Git o descarga de nuevo el proyecto.

---

### 6. ✓ Permisos de Escritura

Verifica que puedas escribir en los directorios de salida.

**Salida esperada:**
```
✓ Escritura en out/                             [OK]
✓ Escritura en JSON/BUGS/                       [OK]
✓ Escritura en JSON/DELIVS/                     [OK]
```

**Si falla:**
```
✗ Escritura en out/                             [ERROR]
```

**Solución:**
```bash
# En Linux/Mac
chmod 755 out/

# En Windows (ejecutar cmd como administrador)
icacls out /grant Users:F
```

---

### 7. ✓ Archivos de Entrada

Verifica que exista el archivo de entrada principal:
- `in/incidencias_in.csv`

**Salida esperada:**
```
✓ incidencias_in.csv                            [OK]
  → Existe (1234 bytes)
```

**Posibles estados:**
```
⚠ incidencias_in.csv                            [ADVERTENCIA]
  → Existe pero está vacío

✗ incidencias_in.csv                            [ERROR]
  → NO EXISTE
```

**Solución:**
1. Crea el archivo `in/incidencias_in.csv`
2. Añade al menos una columna llamada `Incidencia` con los números de incidencia

**Ejemplo:**
```csv
Incidencia
INC000000012345
INC000000067890
```

---

### 8. ✓ Conectividad con Jira

Verifica que puedas conectarte al servidor Jira con tus credenciales.

**Salida esperada:**
```
✓ Conectividad con Jira                         [OK]
  → Conexión exitosa (Status: 404)
```

*Nota: Status 404 es OK, significa que conectó al servidor aunque el issue de prueba no existe.*

**Si falla:**
```
✗ Conectividad con Jira                         [ERROR]
  → Error de configuración: Credenciales de Jira no configuradas
```

o

```
✗ Conectividad con Jira                         [ERROR]
  → Error de conexión: Connection refused
```

**Soluciones:**
1. Verifica que tus credenciales en `.env` sean correctas
2. Verifica que tengas conexión a internet
3. Verifica que la URL de Jira sea accesible
4. Omite esta prueba con `--skip-jira` si no puedes conectar ahora

---

## Interpretación de Resultados

### ✓ ENTORNO VÁLIDO (Todo OK)

```
✓ ENTORNO VÁLIDO
El proyecto está listo para ejecutarse.

Puedes ejecutar:
  • python JiraOrange/jira_bugs_to_json.py
  • python JiraOrange/jira_delivs_to_json.py
  • python JiraOrange/jira_bugs_etl.py
  • python JiraOrange/jira_delivs_etl.py
```

**Acción:** ¡Puedes ejecutar el proyecto sin problemas!

---

### ⚠ ADVERTENCIAS (Funcional pero con avisos)

```
⚠ ADVERTENCIAS (2)
El proyecto puede ejecutarse, pero revisa las advertencias:

  1. Archivo de entrada incidencias_in.csv no encontrado
  2. No se pudo conectar a Jira
```

**Acción:** Puedes ejecutar, pero algunos scripts pueden fallar si dependen de lo advertido.

---

### ✗ ENTORNO NO VÁLIDO (Errores críticos)

```
✗ ENTORNO NO VÁLIDO
Se encontraron 3 errores:

  1. Librerías faltantes
  2. Variable USUARIO no configurada
  3. Variable PASS no configurada

Soluciones rápidas:
  1. Instalar dependencias: pip install -r requirements.txt
  2. Configurar .env: cp .env.example .env && nano .env
  3. Crear directorios: python -c 'import JiraOrange.configD'
```

**Acción:** Debes resolver los errores antes de ejecutar el proyecto.

---

## Códigos de Salida

El script retorna códigos de salida útiles para scripts:

- **0** = Todo OK o solo advertencias (puedes ejecutar)
- **1** = Hay errores críticos (NO ejecutes)

**Uso en scripts:**

```bash
#!/bin/bash

python validar_entorno.py
if [ $? -eq 0 ]; then
    echo "Ejecutando ETL..."
    python JiraOrange/jira_bugs_etl.py
else
    echo "Entorno no válido. Corrige los errores primero."
    exit 1
fi
```

---

## Preguntas Frecuentes

### ¿Debo ejecutar esto cada vez?

No, solo:
- Antes de la primera ejecución
- Después de actualizar el código del repositorio
- Si encuentras errores extraños
- Después de cambiar configuración

### ¿Qué hago si dice "Versión de Python incompatible"?

Instala Python 3.7 o superior desde [python.org](https://www.python.org/downloads/)

Verifica tu versión actual:
```bash
python --version
```

### ¿Por qué falla la conexión a Jira?

Causas comunes:
1. Credenciales incorrectas en `.env`
2. Sin conexión a internet
3. VPN desconectada (si tu Jira requiere VPN)
4. Firewall bloqueando la conexión

Prueba conectar manualmente a la URL de Jira en tu navegador.

### ¿Puedo usar esto en CI/CD?

Sí, es ideal para pipelines:

```yaml
# .github/workflows/validate.yml
name: Validate Environment
on: [push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python validar_entorno.py --skip-jira
```

### ¿Cómo desactivo los colores?

Si no ves bien los colores en tu terminal:

```bash
# Linux/Mac
NO_COLOR=1 python validar_entorno.py

# Windows
set NO_COLOR=1 && python validar_entorno.py
```

---

## Soluciones Rápidas Comunes

### Setup Completo desde Cero

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar credenciales
cp .env.example .env
nano .env  # Editar con tus credenciales

# 4. Crear directorios
python -c "import JiraOrange.configD"

# 5. Validar
python validar_entorno.py

# 6. Si OK, ejecutar
python JiraOrange/jira_bugs_to_json.py
```

### Solo Falta .env

```bash
cp .env.example .env
nano .env  # Completar USUARIO y PASS
python validar_entorno.py
```

### Solo Faltan Librerías

```bash
pip install -r requirements.txt
python validar_entorno.py
```

---

## Ayuda Adicional

Si después de seguir esta guía sigues teniendo problemas:

1. Ejecuta con `--verbose` para más información:
   ```bash
   python validar_entorno.py --verbose
   ```

2. Revisa los archivos de documentación:
   - [README.md](README.md) - Documentación principal
   - [MEJORAS_IMPLEMENTADAS.md](MEJORAS_IMPLEMENTADAS.md) - Cambios recientes

3. Verifica que estés en el directorio correcto:
   ```bash
   pwd  # Debe mostrar .../informe-jira-python
   ```

---

**Última actualización:** 2025-12-02
