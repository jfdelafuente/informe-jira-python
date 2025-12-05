# Tests de Integración

Este directorio contiene tests de integración para verificar la conectividad y autenticación con Jira.

## Tests Disponibles

### test_jira_auth.py

Test completo de autenticación con Jira que verifica:
- Autenticación mediante endpoint `/rest/auth/1/session`
- Información del usuario mediante `/rest/api/2/myself`
- Permisos de lectura mediante búsqueda JQL

**Uso:**
```bash
python tests/integration/test_jira_auth.py
```

### test_jira_ssl.py

Test básico de conectividad SSL con Jira.

**Uso:**
```bash
python tests/integration/test_jira_ssl.py
```

## Requisitos

Antes de ejecutar los tests, asegúrate de tener configurado tu archivo `.env` en la raíz del proyecto con:

```env
USUARIO=tu_usuario_jira
PASS=tu_password
JIRA_VERIFY_SSL=false
```

## Interpretación de Resultados

### Status 200
- Autenticación y permisos correctos

### Status 401
- Credenciales incorrectas
- Verifica USUARIO y PASS en .env

### Status 403
- Usuario autenticado pero sin permisos
- La autenticación básica HTTP puede estar deshabilitada
- Puede requerir OAuth/SSO

### Status 404
- Conexión exitosa pero el recurso no existe
- Indica que la autenticación funciona

## Notas

- Los tests desactivan la verificación SSL (`verify=False`) por defecto
- Se usa autenticación HTTP Basic
- Los logs de requests están silenciados para una salida más limpia
