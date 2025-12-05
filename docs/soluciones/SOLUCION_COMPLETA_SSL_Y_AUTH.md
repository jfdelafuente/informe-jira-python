# Solución Completa: SSL y Autenticación Jira

## ✅ PROBLEMA SSL - RESUELTO

### El Error Original
```
SSLError: certificate verify failed: self signed certificate in certificate chain
```

### La Solución Aplicada

Se agregó soporte para deshabilitar verificación SSL en [JiraAPIHandler.py](JiraOrange/api/JiraAPIHandler.py):

**1. Configuración en `.env`:**
```env
JIRA_VERIFY_SSL=false
```

**2. Modificaciones en JiraAPIHandler:**
- Nuevo parámetro `verify_ssl` en `__init__()`
- Lee `JIRA_VERIFY_SSL` desde `.env`
- Pasa `verify=self._verify_ssl` a requests
- Suprime warnings de SSL cuando está deshabilitado

**Resultado**: ✅ La conexión HTTPS ahora funciona correctamente.

---

## ❌ PROBLEMA ACTUAL - Error 403 Forbidden

### Diagnóstico Ejecutado

```bash
python test_auth.py
```

**Resultados**:
- ✅ Conexión HTTPS establecida (sin error SSL)
- ❌ Status 403 en `/rest/auth/1/session`
- ❌ Status 403 en `/rest/api/2/myself`
- ❌ Status 403 en `/rest/api/latest/search`

### ¿Qué significa?

El servidor Jira está **rechazando la autenticación** en todos los endpoints. Esto indica:

1. **Autenticación Básica HTTP deshabilitada** (más probable)
   - Muchas instancias corporativas de Jira deshabilitan Basic Auth
   - Requieren autenticación SSO/OAuth

2. **Credenciales incorrectas**
   - Usuario: `jdelat`
   - Verifica que sean las mismas que usas en el navegador

3. **Autenticación de dos factores (2FA)**
   - Si Jira requiere 2FA, no puedes usar password directamente
   - Necesitas un API Token

---

## Soluciones Posibles

### 🔑 Solución 1: Usar API Token (Recomendado)

Jira Cloud y muchas instancias Enterprise usan API Tokens en lugar de passwords.

#### Paso 1: Generar API Token

1. Ve a https://jira.si.orange.es
2. Click en tu perfil (esquina superior derecha)
3. Selecciona "Account Settings" o "Configuración"
4. Busca "Security" → "API tokens" o "Create API token"
5. Genera un token y cópialo

#### Paso 2: Actualiza `.env`

```env
USUARIO=jdelat
# Usa el API token en lugar del password
PASSWORD=tu_api_token_aqui

JIRA_VERIFY_SSL=false
```

#### Paso 3: Prueba

```bash
python test_auth.py
```

---

### 🔐 Solución 2: Verificar Credenciales

#### Prueba manual en el navegador:

1. Abre https://jira.si.orange.es
2. Intenta iniciar sesión con:
   - Usuario: `jdelat`
   - Password: (el que tienes en `.env`)

¿Funciona?
- **Sí** → El problema es que Basic Auth está deshabilitado → Usa API Token
- **No** → Credenciales incorrectas → Actualiza `.env`

---

### 🌐 Solución 3: Autenticación SSO/OAuth

Si Jira requiere SSO (como SAML, Active Directory, etc.):

#### Opción A: Usar navegador para obtener cookie

```python
import requests

# 1. Abre navegador y logueate en Jira
# 2. Copia las cookies JSESSIONID o atlassian.xsrf.token
# 3. Úsalas en requests

session = requests.Session()
session.cookies.set('JSESSIONID', 'tu_cookie_aqui')
session.verify = False
response = session.get('https://jira.si.orange.es/rest/api/2/myself')
```

#### Opción B: Contactar TI

Solicita a tu departamento de TI:
- ¿Está habilitada la autenticación básica HTTP?
- ¿Debo usar API Token?
- ¿Qué método de autenticación debo usar para scripts?

---

## Verificar la Solución

### Prueba Rápida

```bash
# Con API Token
python test_auth.py
```

Deberías ver:
```
[OK] Autenticacion valida
Usuario autenticado: Juan De La Fuente
```

### Prueba Completa

```bash
python validar_entorno.py
```

Debería mostrar:
```
[OK] Conectividad con Jira [OK]
  -> Conexión exitosa (Status: 200)
```

---

## Resumen de Configuración

### Archivo `.env` Actual

```env
USUARIO="jdelat"
PASSWORD="!Meloni.2025"

# SSL: Deshabilitar verificación para certificado auto-firmado
JIRA_VERIFY_SSL=false
```

### Próximo Paso CRÍTICO

**ACCIÓN REQUERIDA**: Determinar el método de autenticación correcto.

Ejecuta estos comandos para diagnóstico:

```bash
# 1. Probar con credenciales actuales
python test_auth.py

# 2. Si falla, genera API Token y actualiza .env
# PASSWORD=tu_nuevo_api_token

# 3. Vuelve a probar
python test_auth.py
```

---

## Scripts de Diagnóstico Creados

1. **test_ssl.py** - Verifica conectividad básica
2. **test_auth.py** - Diagnóstico completo de autenticación

Ejecuta estos scripts para identificar el problema exacto.

---

## Estado Actual

| Componente | Estado | Nota |
|------------|--------|------|
| **SSL** | ✅ Resuelto | JIRA_VERIFY_SSL=false funciona |
| **Conexión HTTPS** | ✅ OK | Se establece sin errores |
| **Autenticación** | ❌ Error 403 | Requiere API Token o SSO |
| **Credenciales en .env** | ⚠️ Revisar | Password vs API Token |

---

## Próximos Pasos

1. **Inmediato**: Genera un API Token de Jira
2. **Actualizar**: Reemplaza PASSWORD en `.env` con el token
3. **Probar**: Ejecuta `python test_auth.py`
4. **Si funciona**: Ejecuta `python validar_entorno.py`
5. **Si falla**: Contacta a TI de Orange para método de autenticación

---

**Última actualización**: 2025-12-02
**Estado**: SSL resuelto ✅ | Auth pendiente ⏳
