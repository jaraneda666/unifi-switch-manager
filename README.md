# UniFi Switch VLAN & FastPath Automation

Herramientas de automatización para conmutadores de red UniFi (US-8-60W) mediante la interfaz CLI FastPath por SSH. Automatiza el etiquetado de puertos VLAN trunk/access, auditoría de puertos y escaneo de dispositivos.

---

## Arquitectura y Componentes

- **Conexión:** Sesiones SSH automatizadas hacia la consola FastPath del switch.
- **VLANs:** Aprovisionamiento declarativo de bases de datos de VLAN y asignación de PVID.
- **Inventario:** Escaneo y correlación de direcciones MAC y tablas ARP.

---

## Instrucciones de Uso

```bash
# Auditoría de puertos y VLANs en switch UniFi
python tools/audit_network_devices.py --ip 192.168.1.2
```

---

## Consideraciones de Seguridad

- Este repositorio almacena código fuente, utilitarios de prueba y documentación técnica de ingeniería.
- Todas las credenciales, llaves privadas y variables de entorno deben suministrarse de forma local mediante archivos no versionados.
- Las herramientas de auditoría contenidas deben utilizarse exclusivamente en entornos autorizados y laboratorios de prueba.

---

**Autor:** Security Analyst  
**Licencia:** Uso Privado / Propietario
