# Solución al Error de Certificado SSL

## El Problema

```
SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED]
certificate verify failed: self signed certificate in certificate chain
```

Este error ocurre cuando el servidor Jira usa un **certificado SSL auto-firmado** que Python no puede verificar.

---

## Soluciones (en orden de preferencia)

### ✅ Solución 1: Deshabilitar Verificación SSL (Desarrollo)

**La más rápida** - Recomendada para entornos de desarrollo/testing interno.

#### Paso 1: Edita tu archivo `.env`

```env
# Credenciales de Jira
USUARIO=tu_usuario
PASS=tu_password

# Deshabilitar verificación SSL
JIRA_VERIFY_SSL=false
```

#### Paso 2: Ejecuta tu script

```bash
python validar_entorno.py
```

¡Listo! El cliente ahora acepta certificados auto-firmados.

**⚠️ ADVERTENCIA**: Solo usar en desarrollo. **NUNCA** deshabilitar SSL en producción.

---

### 🔒 Solución 2: Instalar el Certificado (Producción)

**Más segura** - Recomendada para producción.

#### Windows

1. **Obtener el certificado**:
   - Abre el navegador (Chrome/Firefox)
   - Ve a `https://jira.si.orange.es`
   - Click en el candado 🔒 → "Certificado"
   - Click en "Detalles" → "Copiar a archivo"
   - Guarda como `jira-cert.crt`

2. **Instalar el certificado**:
   ```cmd
   # Doble click en jira-cert.crt
   # O usar certmgr.msc (Administrador de certificados)
   ```

3. **Indicar la ruta en Python**:

   Opción A - En `.env`:
   ```env
   JIRA_SSL_CERT_PATH=C:/ruta/al/jira-cert.crt
   ```

   Opción B - Usar variable de entorno del sistema:
   ```cmd
   set REQUESTS_CA_BUNDLE=C:\ruta\al\jira-cert.crt
   ```

#### Linux/Mac

1. **Obtener el certificado**:
   ```bash
   # Descargar certificado del servidor
   echo | openssl s_client -connect jira.si.orange.es:443 2>/dev/null | \
       openssl x509 > jira-cert.crt
   ```

2. **Instalar certificado**:

   **Ubuntu/Debian**:
   ```bash
   sudo cp jira-cert.crt /usr/local/share/ca-certificates/
   sudo update-ca-certificates
   ```

   **RHEL/CentOS**:
   ```bash
   sudo cp jira-cert.crt /etc/pki/ca-trust/source/anchors/
   sudo update-ca-trust
   ```

   **macOS**:
   ```bash
   sudo security add-trusted-cert -d -r trustRoot \
       -k /Library/Keychains/System.keychain jira-cert.crt
   ```

3. **Usar variable de entorno**:
   ```bash
   export REQUESTS_CA_BUNDLE=/ruta/al/jira-cert.crt
   python validar_entorno.py
   ```

---

### 🔧 Solución 3: Deshabilitar SSL Programáticamente

Si no puedes editar `.env`, puedes hacerlo en el código:

```python
from JiraOrange.api.JiraAPIHandler import JiraAPIHandler

# Crear cliente con SSL deshabilitado
jira = JiraAPIHandler(verify_ssl=False)

# Usar normalmente
status, bugs = jira.get_bug_to_json("INC000000012345")
```

---

## Verificar la Solución

Una vez aplicada cualquier solución, ejecuta:

```bash
python validar_entorno.py
```

Deberías ver:

```
[OK] Conectividad con Jira                         [OK]
  -> Conexión exitosa (Status: 200)
```

O si el issue TEST-1 no existe (pero conectó):

```
[OK] Conectividad con Jira                         [OK]
  -> Conexión exitosa (Status: 404)
```

---

## Explicación Técnica

### ¿Por qué ocurre este error?

El servidor `jira.si.orange.es` usa un certificado SSL firmado por una autoridad certificadora (CA) interna de la empresa, no reconocida por Python/requests.

### ¿Qué hace cada solución?

| Solución | Cómo funciona | Seguridad | Uso |
|----------|---------------|-----------|-----|
| **Deshabilitar SSL** | `verify=False` en requests | ⚠️ Baja | Desarrollo |
| **Instalar certificado** | Agrega CA al trust store | ✅ Alta | Producción |
| **Variable REQUESTS_CA_BUNDLE** | Especifica certificado válido | ✅ Alta | Producción |

---

## Configuración Avanzada

### Usar Certificado Específico en JiraAPIHandler

Modificar `__init__` para aceptar ruta de certificado:

```python
# En tu script
jira = JiraAPIHandler(
    verify_ssl='/ruta/al/certificado.crt'  # Ahora acepta str con ruta
)
```

Para habilitar esto, el código actual necesita modificación. Abre un issue si lo necesitas.

---

## Troubleshooting

### ❌ Error: "urllib3 module not found"

```bash
pip install urllib3
```

### ❌ Error persiste después de instalar certificado

1. Verificar que Python use el certificado correcto:
   ```python
   import requests
   print(requests.certs.where())
   ```

2. Forzar uso del certificado:
   ```bash
   export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
   ```

### ❌ Warning: "InsecureRequestWarning"

Esto es normal cuando `JIRA_VERIFY_SSL=false`. Para suprimirlo:

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

(Ya incluido en el código mejorado)

---

## Recomendación Final

**Para tu caso específico (jira.si.orange.es)**:

1. **Desarrollo/Testing**: Usa `JIRA_VERIFY_SSL=false` en `.env` ✅
2. **Producción**: Solicita a IT el certificado de la CA interna y úsalo con `REQUESTS_CA_BUNDLE`

El servidor `jira.si.orange.es` es interno de Orange, así que es seguro deshabilitar SSL en desarrollo.

---

## Resumen Rápido

### Para Resolver AHORA (30 segundos):

1. Edita `.env`:
   ```env
   JIRA_VERIFY_SSL=false
   ```

2. Ejecuta:
   ```bash
   python validar_entorno.py
   ```

✅ **Problema resuelto**

---

**Última actualización**: 2025-12-02
**Versión de JiraAPIHandler**: 2.1 (con soporte SSL configurable)
