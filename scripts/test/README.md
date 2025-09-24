# test

Script para probar conectividad y funcionalidad de la base de datos PostgreSQL a través del API Gateway.

## ¿Qué hace?

- 🔍 **Verifica conectividad** - Health check del servicio de base de datos
- 📊 **Obtiene información** - Versión, usuario, estadísticas de PostgreSQL
- 📋 **Lista tablas** - Muestra todas las tablas en la base de datos
- 🔍 **Ejecuta queries** - Permite ejecutar SQL personalizado
- 🧪 **Testing completo** - Suite de pruebas automatizadas
- 📈 **Métricas** - Tiempo de respuesta y performance

## Flags disponibles

- `--endpoint="health|info|tables|query|test-all"` - Endpoint específico a probar (default: test-all)
- `--query="SQL"` - Query SQL personalizada cuando endpoint=query
- `--verbose` - Mostrar información detallada (default: false)
- `--timeout=30` - Timeout en segundos para requests (default: 30)
- `--url="http://localhost:4321"` - URL base del API Gateway (default: http://localhost:4321)
- `--user="admin"` - Usuario de autenticación (default: admin)
- `--password="portfolio_admin"` - Password de autenticación (default: portfolio_admin)

## Ejemplos de uso

### Testing completo
```bash
python scripts/run.py test
```

### Health check específico
```bash
python scripts/run.py test --endpoint="health" --verbose
```

### Información de la base de datos
```bash
python scripts/run.py test --endpoint="info"
```

### Listar tablas
```bash
python scripts/run.py test --endpoint="tables" --verbose
```

### Ejecutar query personalizada
```bash
python scripts/run.py test --endpoint="query" --query="SELECT version();"
python scripts/run.py test --endpoint="query" --query="SELECT current_database(), current_user;"
```

### Con configuración personalizada
```bash
python scripts/run.py test --url="http://localhost:4321" --user="admin" --password="portfolio_admin" --verbose
```

### Testing con timeout personalizado
```bash
python scripts/run.py test --endpoint="test-all" --timeout=60 --verbose
```

## Casos de uso comunes

- **Verificar después de levantar servicios**: Confirmar que la base de datos está operativa
- **Debug de conectividad**: Diagnosticar problemas de conexión
- **Monitoreo de performance**: Medir tiempos de respuesta
- **Testing de queries**: Probar SQL antes de implementar en código
- **Validación de deployment**: Verificar que todo funciona en diferentes entornos