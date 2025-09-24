"""
Visualización de información de conexión a la base de datos.
"""

import os
from typing import List


def show_database_connection_info(services_list: List[str], verbose: bool = False):
    """
    Muestra información de conexión a PostgreSQL si se levantó el servicio de DB.

    Args:
        services_list: Lista de servicios levantados
        verbose: Mostrar información detallada
    """
    # Verificar si se levantó la base de datos
    db_services = ['db', 'database', 'postgres', 'postgresql']
    db_requested = any(
        any(db_service in service.lower() for db_service in db_services)
        for service in services_list
    ) or 'all' in services_list

    if not db_requested:
        return

    print("\n" + "="*60)
    print("🗄️  INFORMACIÓN DE CONEXIÓN POSTGRESQL")
    print("="*60)

    # Información básica de conexión
    db_info = {
        'host': 'localhost',
        'port': '5432',
        'database': 'portfolio_local',
        'username': 'postgres',
        'password': 'portfolio_password'
    }

    print(f"\n📋 Acceso a la base de datos:")
    print(f"   🚨 IMPORTANTE: La base de datos NO está expuesta directamente")
    print(f"   🌐 Solo accesible a través del API Gateway en puerto 4321")
    print(f"   🔒 Requiere autenticación básica para seguridad")

    # URL de acceso a través del API Gateway
    gateway_port = "4321"
    db_admin_url = f"http://localhost:{gateway_port}/db"

    print(f"\n🔗 URL de acceso (API Gateway):")
    print(f"   Database Admin:  {db_admin_url}")

    # Información de autenticación
    auth_info = {
        'admin_user': 'admin',
        'admin_password': 'portfolio_admin'
    }

    print(f"\n🔐 Credenciales de acceso:")
    print(f"   Usuario:  {auth_info['admin_user']}")
    print(f"   Password: {auth_info['admin_password']}")

    # Comandos de ejemplo usando curl
    print(f"\n🛠️  Comandos de ejemplo (REST API):")
    print(f"   # Health check del admin DB")
    print(f"   curl -u {auth_info['admin_user']}:{auth_info['admin_password']} {db_admin_url}/health")
    print(f"")
    print(f"   # Listar tablas")
    print(f"   curl -u {auth_info['admin_user']}:{auth_info['admin_password']} {db_admin_url}/tables")
    print(f"")
    print(f"   # Ejecutar query SQL")
    print(f"   curl -u {auth_info['admin_user']}:{auth_info['admin_password']} \\")
    print(f"        -X POST {db_admin_url}/query \\")
    print(f"        -H 'Content-Type: application/json' \\")
    print(f"        -d '{{\"sql\": \"SELECT version();\"}}'")
    print(f"")
    print(f"   # Ver información de la base de datos")
    print(f"   curl -u {auth_info['admin_user']}:{auth_info['admin_password']} {db_admin_url}/info")
    print(f"")
    print(f"   # Interfaz web de administración")
    print(f"   open {db_admin_url}")
    print(f"   # (Se abrirá en el navegador - requiere autenticación)")

    # Información interna (solo para contenedores)
    print(f"\n🐳 Acceso interno (solo contenedores Docker):")
    print(f"   Host interno:     portfolio-db")
    print(f"   Puerto interno:   5432")
    print(f"   Base de datos:    {db_info['database']}")
    print(f"   Usuario:          {db_info['username']}")
    print(f"   Password:         {db_info['password']}")

    # Comandos Docker para administración directa
    print(f"\n🔧 Administración directa (Docker):")
    print(f"   # Ver logs de la base de datos")
    print(f"   docker logs portfolio-db")
    print(f"")
    print(f"   # Conectar directamente al contenedor")
    print(f"   docker exec -it portfolio-db psql -U {db_info['username']} -d {db_info['database']}")
    print(f"")
    print(f"   # Ejecutar query directo en el contenedor")
    print(f"   docker exec portfolio-db psql -U {db_info['username']} -d {db_info['database']} -c 'SELECT version();'")
    print(f"")
    print(f"   # Backup de la base de datos")
    print(f"   docker exec portfolio-db pg_dump -U {db_info['username']} {db_info['database']} > backup.sql")

    # Crear archivo de ejemplo actualizado
    create_connection_example_file(db_info, verbose, gateway_port, auth_info)

    if verbose:
        print(f"\n📄 Variables de entorno recomendadas:")
        print(f"   # Para contenedores internos:")
        print(f"   DATABASE_URL=postgresql://{db_info['username']}:{db_info['password']}@portfolio-db:5432/{db_info['database']}")
        print(f"   # Para acceso via API Gateway:")
        print(f"   DB_ADMIN_URL=http://localhost:{gateway_port}/db")
        print(f"   DB_ADMIN_USER={auth_info['admin_user']}")
        print(f"   DB_ADMIN_PASSWORD={auth_info['admin_password']}")
        print(f"   DB_HOST={db_info['host']}")
        print(f"   DB_PORT={db_info['port']}")
        print(f"   DB_NAME={db_info['database']}")
        print(f"   DB_USER={db_info['username']}")
        print(f"   DB_PASSWORD={db_info['password']}")

    print("="*60)


def create_connection_example_file(db_info: dict, verbose: bool = False, gateway_port: str = "4321", auth_info: dict = None):
    """
    Crea un archivo de ejemplo con comandos de conexión a PostgreSQL a través del API Gateway.

    Args:
        db_info: Información de la base de datos
        verbose: Mostrar información detallada
        gateway_port: Puerto del API Gateway (default: 4321)
        auth_info: Información de autenticación
    """
    if auth_info is None:
        auth_info = {'admin_user': 'admin', 'admin_password': 'portfolio_admin'}

    try:
        # Contenido del archivo de ejemplo
        example_content = f"""#!/bin/bash
# Archivo de ejemplo para conectar a PostgreSQL a través del API Gateway
# Generado automáticamente por el sistema setup
#
# 🚨 IMPORTANTE: La base de datos NO está expuesta directamente
# Solo es accesible a través del API Gateway en puerto {gateway_port}

# ==============================================
# CONFIGURACIÓN DEL API GATEWAY
# ==============================================

# URLs del API Gateway
export GATEWAY_PORT="{gateway_port}"
export DB_ADMIN_URL="http://localhost:${{GATEWAY_PORT}}/db"

# Credenciales de acceso (autenticación básica)
export ADMIN_USER="{auth_info['admin_user']}"
export ADMIN_PASSWORD="{auth_info['admin_password']}"

# ==============================================
# COMANDOS REST API PARA BASE DE DATOS
# ==============================================

# Función para verificar health check
db_health_check() {{
    echo "🏥 Verificando estado de la base de datos..."
    curl -u $ADMIN_USER:$ADMIN_PASSWORD \\
         -s \\
         "$DB_ADMIN_URL/health" | jq .
}}

# Función para obtener información de la base de datos
db_info() {{
    echo "📊 Información de la base de datos:"
    curl -u $ADMIN_USER:$ADMIN_PASSWORD \\
         -s \\
         "$DB_ADMIN_URL/info" | jq .
}}

# Función para listar tablas
db_list_tables() {{
    echo "📋 Tablas en la base de datos:"
    curl -u $ADMIN_USER:$ADMIN_PASSWORD \\
         -s \\
         "$DB_ADMIN_URL/tables" | jq .
}}

# Función para ejecutar una query SQL
db_query() {{
    local sql_query="$1"
    if [ -z "$sql_query" ]; then
        echo "Usage: db_query 'SELECT * FROM table_name;'"
        return 1
    fi

    echo "🔍 Ejecutando query: $sql_query"
    curl -u $ADMIN_USER:$ADMIN_PASSWORD \\
         -s \\
         -X POST \\
         -H "Content-Type: application/json" \\
         -d "{{\"sql\": \"$sql_query\"}}" \\
         "$DB_ADMIN_URL/query" | jq .
}}

# Función para obtener esquema de una tabla
db_describe_table() {{
    local table_name="$1"
    if [ -z "$table_name" ]; then
        echo "Usage: db_describe_table 'table_name'"
        return 1
    fi

    echo "🏗️  Estructura de la tabla $table_name:"
    curl -u $ADMIN_USER:$ADMIN_PASSWORD \\
         -s \\
         "$DB_ADMIN_URL/tables/$table_name/schema" | jq .
}}

# ==============================================
# EJEMPLOS DE USO COMÚN
# ==============================================

# Ejemplos de comandos básicos
example_commands() {{
    echo "🎯 Ejemplos de comandos disponibles:"
    echo ""
    echo "# Verificar estado"
    echo "db_health_check"
    echo ""
    echo "# Ver información general"
    echo "db_info"
    echo ""
    echo "# Listar tablas"
    echo "db_list_tables"
    echo ""
    echo "# Ejecutar query personalizada"
    echo "db_query 'SELECT version();'"
    echo "db_query 'SELECT NOW();'"
    echo "db_query 'SELECT * FROM pg_stat_database;'"
    echo ""
    echo "# Ver estructura de tabla"
    echo "db_describe_table 'users'"
    echo ""
    echo "# Acceder a interfaz web de administración"
    echo "echo 'Abrir en navegador: $DB_ADMIN_URL'"
    echo "echo 'Usuario: $ADMIN_USER'"
    echo "echo 'Password: $ADMIN_PASSWORD'"
}}

# ==============================================
# ACCESO DIRECTO DOCKER (ADMIN AVANZADO)
# ==============================================

# Información de la base de datos interna (solo contenedores)
export DB_HOST_INTERNAL="{db_info['host']}"
export DB_PORT_INTERNAL="{db_info['port']}"
export DB_NAME_INTERNAL="{db_info['database']}"
export DB_USER_INTERNAL="{db_info['username']}"
export DB_PASSWORD_INTERNAL="{db_info['password']}"

# Comando directo al contenedor (bypass del API Gateway)
docker_psql() {{
    echo "🐳 Conectando directamente al contenedor PostgreSQL..."
    docker exec -it portfolio-db psql -U $DB_USER_INTERNAL -d $DB_NAME_INTERNAL
}}

# Ejecutar query directo en contenedor
docker_query() {{
    local sql_query="$1"
    if [ -z "$sql_query" ]; then
        echo "Usage: docker_query 'SELECT * FROM table_name;'"
        return 1
    fi

    echo "🐳 Ejecutando query directa en contenedor: $sql_query"
    docker exec portfolio-db psql -U $DB_USER_INTERNAL -d $DB_NAME_INTERNAL -c "$sql_query"
}}

# Backup directo desde contenedor
docker_backup() {{
    local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
    echo "💾 Creando backup: $backup_file"
    docker exec portfolio-db pg_dump -U $DB_USER_INTERNAL $DB_NAME_INTERNAL > "$backup_file"
    echo "✅ Backup creado: $backup_file"
}}

# Ver logs de la base de datos
docker_logs() {{
    echo "📊 Logs de PostgreSQL:"
    docker logs portfolio-db
}}

# ==============================================
# TESTING COMPLETO DEL SISTEMA
# ==============================================

# Función de testing completo
test_database_system() {{
    echo "🧪 Testing completo del sistema de base de datos..."
    echo ""

    # Test 1: Health check del API Gateway
    echo "1️⃣  Testing health check del API Gateway..."
    if curl -u $ADMIN_USER:$ADMIN_PASSWORD -s "$DB_ADMIN_URL/health" | grep -q "healthy"; then
        echo "✅ API Gateway respondiendo correctamente"
    else
        echo "❌ API Gateway no responde o no está healthy"
    fi

    # Test 2: Conexión a la base de datos
    echo ""
    echo "2️⃣  Testing conexión a la base de datos..."
    if docker exec portfolio-db pg_isready -U $DB_USER_INTERNAL -d $DB_NAME_INTERNAL > /dev/null 2>&1; then
        echo "✅ Base de datos PostgreSQL accesible"
    else
        echo "❌ Base de datos PostgreSQL no accesible"
    fi

    # Test 3: Query básica a través del API
    echo ""
    echo "3️⃣  Testing query a través del API..."
    if db_query "SELECT 1 as test;" | grep -q "test"; then
        echo "✅ Queries a través del API funcionando"
    else
        echo "❌ Error ejecutando queries a través del API"
    fi

    # Test 4: Listar tablas
    echo ""
    echo "4️⃣  Testing listado de tablas..."
    if db_list_tables | grep -q "tables"; then
        echo "✅ Listado de tablas funcionando"
    else
        echo "❌ Error listando tablas"
    fi

    echo ""
    echo "🎉 Testing completado!"
}}

# ==============================================
# MENÚ INTERACTIVO
# ==============================================

# Menú principal
main_menu() {{
    echo ""
    echo "🗄️  PORTFOLIO DATABASE ADMIN - API GATEWAY ACCESS"
    echo "=================================================="
    echo ""
    echo "Selecciona una opción:"
    echo ""
    echo "1) Health check del sistema"
    echo "2) Ver información de la base de datos"
    echo "3) Listar tablas"
    echo "4) Ejecutar query personalizada"
    echo "5) Abrir interfaz web de administración"
    echo "6) Testing completo del sistema"
    echo "7) Acceso directo Docker (avanzado)"
    echo "8) Ver ejemplos de comandos"
    echo "9) Salir"
    echo ""
    read -p "Opción: " choice

    case $choice in
        1) db_health_check ;;
        2) db_info ;;
        3) db_list_tables ;;
        4)
            read -p "SQL Query: " query
            db_query "$query"
            ;;
        5)
            echo "🌐 Interfaz web de administración:"
            echo "URL: $DB_ADMIN_URL"
            echo "Usuario: $ADMIN_USER"
            echo "Password: $ADMIN_PASSWORD"
            ;;
        6) test_database_system ;;
        7) docker_psql ;;
        8) example_commands ;;
        9) echo "👋 ¡Hasta luego!"; exit 0 ;;
        *) echo "❌ Opción inválida" ;;
    esac
}}

# ==============================================
# EJECUCIÓN
# ==============================================

# Mostrar información inicial
echo "🗄️  PORTFOLIO DATABASE ACCESS - API GATEWAY"
echo "============================================="
echo ""
echo "🌐 Base URL: http://localhost:{gateway_port}"
echo "🔗 Database Admin: $DB_ADMIN_URL"
echo "👤 Usuario: $ADMIN_USER"
echo "🔐 Password: $ADMIN_PASSWORD"
echo ""
echo "📖 Ejecuta 'main_menu' para acceder al menú interactivo"
echo "📚 Ejecuta 'example_commands' para ver ejemplos de uso"
echo ""

# Descomenta para ejecutar el menú automáticamente
# main_menu
"""

        # Información sobre el script de testing integrado
        print(f"\n🧪 Script de testing de base de datos:")
        print(f"   Testing completo:     python scripts/run.py test")
        print(f"   Health check:         python scripts/run.py test --endpoint=health")
        print(f"   Info de BD:           python scripts/run.py test --endpoint=info --verbose")
        print(f"   Listar tablas:        python scripts/run.py test --endpoint=tables")
        print(f"   Query personalizada:  python scripts/run.py test --endpoint=query --query=\"SELECT version();\"")
        print(f"   Ayuda del script:     python scripts/run.py test --help")

    except Exception as e:
        if verbose:
            print(f"⚠️  Error mostrando información: {e}")


def get_database_status():
    """
    Obtiene el estado actual de la base de datos PostgreSQL.

    Returns:
        dict: Estado de la base de datos con información detallada
    """
    import subprocess

    try:
        # Verificar si el contenedor está corriendo
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}\t{{.Status}}", "--filter", "name=portfolio-db"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if "portfolio-db" in result.stdout:
            status_line = result.stdout.strip()
            status_parts = status_line.split('\t')
            container_status = status_parts[1] if len(status_parts) > 1 else "Unknown"

            return {
                'running': True,
                'container_name': 'portfolio-db',
                'status': container_status,
                'accessible': True
            }
        else:
            return {
                'running': False,
                'container_name': None,
                'status': 'Not running',
                'accessible': False
            }

    except Exception as e:
        return {
            'running': False,
            'container_name': None,
            'status': f'Error: {e}',
            'accessible': False
        }


def show_database_health_check(verbose: bool = False):
    """
    Muestra un health check específico para la base de datos.

    Args:
        verbose: Mostrar información detallada
    """
    db_status = get_database_status()

    print(f"\n🏥 HEALTH CHECK - BASE DE DATOS")
    print("-" * 35)

    if db_status['running']:
        print(f"✅ Contenedor: {db_status['container_name']}")
        print(f"📊 Estado: {db_status['status']}")

        # Intentar ping a la base de datos
        try:
            import subprocess
            ping_result = subprocess.run(
                ["pg_isready", "-h", "localhost", "-p", "5432"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if ping_result.returncode == 0:
                print("✅ Base de datos respondiendo")
            else:
                print("⚠️  Base de datos no responde a ping")
                if verbose:
                    print(f"   Error: {ping_result.stderr}")

        except Exception as e:
            print("⚠️  No se pudo verificar ping de BD")
            if verbose:
                print(f"   Error: {e}")
    else:
        print("❌ Contenedor no está corriendo")
        print(f"📊 Estado: {db_status['status']}")