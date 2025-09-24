"""
Database Testing Script - Prueba conectividad y funcionalidad de PostgreSQL via API Gateway
"""

import json
import sys
import time
from typing import Dict, Any, Optional
import urllib.request
import urllib.parse
import urllib.error
import base64

def main(flags: Dict[str, Any]):
    """
    Función principal del script de testing de base de datos.

    Args:
        flags (dict): Diccionario con las flags procesadas y validadas
    """
    verbose = flags.get('verbose', False)
    endpoint = flags.get('endpoint', 'test-all')

    if verbose:
        print("🗄️  PORTFOLIO DATABASE TESTING")
        print("=" * 50)
        print()

    # Configurar autenticación
    auth_string = f"{flags['user']}:{flags['password']}"
    auth_bytes = auth_string.encode('ascii')
    auth_base64 = base64.b64encode(auth_bytes).decode('ascii')

    if endpoint == 'test-all':
        run_complete_test_suite(flags, auth_base64, verbose)
    elif endpoint == 'health':
        test_health_endpoint(flags, auth_base64, verbose)
    elif endpoint == 'info':
        test_info_endpoint(flags, auth_base64, verbose)
    elif endpoint == 'tables':
        test_tables_endpoint(flags, auth_base64, verbose)
    elif endpoint == 'query':
        test_query_endpoint(flags, auth_base64, verbose)

def make_request(url: str, auth_base64: str, timeout: int, data: Optional[str] = None, verbose: bool = False) -> Dict[str, Any]:
    """
    Realizar request HTTP con autenticación básica.

    Args:
        url: URL del endpoint
        auth_base64: Autenticación básica codificada
        timeout: Timeout en segundos
        data: Datos JSON para POST requests
        verbose: Mostrar información detallada

    Returns:
        Dict con response, tiempo y metadata
    """
    start_time = time.time()

    # Crear request
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Basic {auth_base64}')

    if data:
        req.add_header('Content-Type', 'application/json')
        req.data = data.encode('utf-8')

    try:
        if verbose:
            method = 'POST' if data else 'GET'
            print(f"  🌐 {method} {url}")
            if data:
                print(f"  📤 Data: {data}")

        with urllib.request.urlopen(req, timeout=timeout) as response:
            response_data = response.read().decode('utf-8')
            response_time = (time.time() - start_time) * 1000

            # Parsear JSON
            try:
                json_data = json.loads(response_data)
            except json.JSONDecodeError:
                json_data = {"raw_response": response_data}

            result = {
                "success": True,
                "status_code": response.getcode(),
                "data": json_data,
                "response_time_ms": response_time,
                "url": url
            }

            if verbose:
                print(f"  ✅ Status: {response.getcode()}")
                print(f"  ⏱️  Time: {response_time:.2f}ms")

            return result

    except urllib.error.HTTPError as e:
        response_time = (time.time() - start_time) * 1000
        error_data = e.read().decode('utf-8') if e.fp else str(e)

        result = {
            "success": False,
            "status_code": e.code,
            "error": error_data,
            "response_time_ms": response_time,
            "url": url
        }

        if verbose:
            print(f"  ❌ HTTP Error: {e.code}")
            print(f"  ⏱️  Time: {response_time:.2f}ms")
            print(f"  📄 Error: {error_data}")

        return result

    except urllib.error.URLError as e:
        response_time = (time.time() - start_time) * 1000

        result = {
            "success": False,
            "status_code": 0,
            "error": str(e.reason),
            "response_time_ms": response_time,
            "url": url
        }

        if verbose:
            print(f"  ❌ Connection Error: {e.reason}")
            print(f"  ⏱️  Time: {response_time:.2f}ms")

        return result

    except Exception as e:
        response_time = (time.time() - start_time) * 1000

        result = {
            "success": False,
            "status_code": 0,
            "error": str(e),
            "response_time_ms": response_time,
            "url": url
        }

        if verbose:
            print(f"  ❌ Unexpected Error: {e}")
            print(f"  ⏱️  Time: {response_time:.2f}ms")

        return result

def test_health_endpoint(flags: Dict[str, Any], auth_base64: str, verbose: bool):
    """Probar endpoint /health"""
    print("🏥 Testing Health Endpoint")
    print("-" * 30)

    url = f"{flags['url']}/db/health"
    result = make_request(url, auth_base64, flags['timeout'], verbose=verbose)

    if result['success']:
        data = result['data']
        status = data.get('status', 'unknown')
        db_connected = data.get('database_connected', False)

        if status == 'healthy' and db_connected:
            print(f"✅ Database is healthy and connected")
        elif status == 'healthy':
            print(f"⚠️  Service is healthy but database not connected")
        else:
            print(f"❌ Service status: {status}")

        if verbose:
            print(f"📊 Service: {data.get('service', 'unknown')}")
            print(f"🕐 Timestamp: {data.get('timestamp', 'unknown')}")

    else:
        print(f"❌ Health check failed: {result['error']}")

    print()

def test_info_endpoint(flags: Dict[str, Any], auth_base64: str, verbose: bool):
    """Probar endpoint /info"""
    print("📊 Testing Database Info Endpoint")
    print("-" * 35)

    url = f"{flags['url']}/db/info"
    result = make_request(url, auth_base64, flags['timeout'], verbose=verbose)

    if result['success']:
        data = result['data']
        print(f"✅ Database info retrieved successfully")
        print(f"🗄️  Version: {data.get('version', 'unknown')}")
        print(f"📦 Database: {data.get('current_database', 'unknown')}")
        print(f"👤 User: {data.get('current_user', 'unknown')}")
        print(f"📋 Tables: {data.get('total_tables', 0)}")
        print(f"🔌 Connections: {data.get('connection_count', 0)}")
    else:
        print(f"❌ Info request failed: {result['error']}")

    print()

def test_tables_endpoint(flags: Dict[str, Any], auth_base64: str, verbose: bool):
    """Probar endpoint /tables"""
    print("📋 Testing Tables Listing Endpoint")
    print("-" * 37)

    url = f"{flags['url']}/db/tables"
    result = make_request(url, auth_base64, flags['timeout'], verbose=verbose)

    if result['success']:
        data = result['data']
        tables = data.get('tables', [])
        total_count = data.get('total_count', 0)

        print(f"✅ Tables listed successfully")
        print(f"📊 Total tables: {total_count}")

        if tables and verbose:
            print("📋 Tables found:")
            for table in tables:
                name = table.get('table_name', 'unknown')
                schema = table.get('table_schema', 'unknown')
                table_type = table.get('table_type', 'unknown')
                print(f"  - {schema}.{name} ({table_type})")
        elif total_count == 0:
            print("📭 No tables found (empty database)")

    else:
        print(f"❌ Tables request failed: {result['error']}")

    print()

def test_query_endpoint(flags: Dict[str, Any], auth_base64: str, verbose: bool):
    """Probar endpoint /query con SQL personalizado"""
    query = flags.get('query', 'SELECT version();')

    print("🔍 Testing Custom Query Endpoint")
    print("-" * 35)
    print(f"📝 Query: {query}")

    url = f"{flags['url']}/db/query"
    data = json.dumps({"sql": query})
    result = make_request(url, auth_base64, flags['timeout'], data=data, verbose=verbose)

    if result['success']:
        data = result['data']
        rows = data.get('rows', [])
        row_count = data.get('row_count', 0)
        execution_time = data.get('execution_time_ms', 0)

        print(f"✅ Query executed successfully")
        print(f"📊 Rows returned: {row_count}")
        print(f"⏱️  Execution time: {execution_time:.2f}ms")

        if rows and verbose:
            print("📋 Results:")
            for i, row in enumerate(rows[:5]):  # Mostrar máximo 5 filas
                print(f"  Row {i+1}: {json.dumps(row, indent=4)}")
            if len(rows) > 5:
                print(f"  ... and {len(rows) - 5} more rows")

    else:
        print(f"❌ Query failed: {result['error']}")

    print()

def run_complete_test_suite(flags: Dict[str, Any], auth_base64: str, verbose: bool):
    """Ejecutar suite completa de pruebas"""
    print("🧪 Running Complete Database Test Suite")
    print("=" * 45)
    print()

    # Métricas globales
    total_start_time = time.time()
    test_results = []

    # Test 1: Health Check
    print("🏥 Test 1: Health Check")
    health_result = test_health_check(flags, auth_base64, verbose)
    test_results.append(("Health Check", health_result))

    # Test 2: Database Info
    print("📊 Test 2: Database Information")
    info_result = test_database_info(flags, auth_base64, verbose)
    test_results.append(("Database Info", info_result))

    # Test 3: Tables Listing
    print("📋 Test 3: Tables Listing")
    tables_result = test_tables_listing(flags, auth_base64, verbose)
    test_results.append(("Tables Listing", tables_result))

    # Test 4: Basic Queries
    print("🔍 Test 4: Basic SQL Queries")
    query_result = test_basic_queries(flags, auth_base64, verbose)
    test_results.append(("Basic Queries", query_result))

    # Test 5: Performance Test
    print("⚡ Test 5: Performance Test")
    perf_result = test_performance(flags, auth_base64, verbose)
    test_results.append(("Performance", perf_result))

    # Resumen final
    total_time = (time.time() - total_start_time) * 1000
    print("📋 Test Results Summary")
    print("=" * 25)

    passed = 0
    failed = 0

    for test_name, result in test_results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        time_str = f"{result['response_time_ms']:.1f}ms"
        print(f"{status} {test_name:<20} ({time_str})")

        if result['success']:
            passed += 1
        else:
            failed += 1

    print()
    print(f"📊 Summary: {passed} passed, {failed} failed")
    print(f"⏱️  Total time: {total_time:.1f}ms")

    if failed > 0:
        print("❌ Some tests failed. Check database configuration.")
        sys.exit(1)
    else:
        print("✅ All tests passed! Database is fully operational.")

def test_health_check(flags: Dict[str, Any], auth_base64: str, verbose: bool) -> Dict[str, Any]:
    """Test health check endpoint"""
    url = f"{flags['url']}/db/health"
    result = make_request(url, auth_base64, flags['timeout'], verbose=verbose)

    if result['success']:
        data = result['data']
        status = data.get('status', 'unknown')
        db_connected = data.get('database_connected', False)

        if status == 'healthy' and db_connected:
            print("  ✅ Service healthy and database connected")
        else:
            print(f"  ⚠️  Status: {status}, DB Connected: {db_connected}")
            result['success'] = False

    print()
    return result

def test_database_info(flags: Dict[str, Any], auth_base64: str, verbose: bool) -> Dict[str, Any]:
    """Test database info endpoint"""
    url = f"{flags['url']}/db/info"
    result = make_request(url, auth_base64, flags['timeout'], verbose=verbose)

    if result['success']:
        data = result['data']
        version = data.get('version', 'unknown')
        database = data.get('current_database', 'unknown')
        print(f"  ✅ PostgreSQL: {version[:50]}...")
        print(f"  📦 Database: {database}")

    print()
    return result

def test_tables_listing(flags: Dict[str, Any], auth_base64: str, verbose: bool) -> Dict[str, Any]:
    """Test tables listing endpoint"""
    url = f"{flags['url']}/db/tables"
    result = make_request(url, auth_base64, flags['timeout'], verbose=verbose)

    if result['success']:
        data = result['data']
        total_count = data.get('total_count', 0)
        print(f"  ✅ Found {total_count} tables")

    print()
    return result

def test_basic_queries(flags: Dict[str, Any], auth_base64: str, verbose: bool) -> Dict[str, Any]:
    """Test basic SQL queries"""
    queries = [
        "SELECT 1 as test_number;",
        "SELECT current_timestamp;",
        "SELECT current_user, current_database();"
    ]

    url = f"{flags['url']}/db/query"
    all_success = True
    total_time = 0

    for i, query in enumerate(queries, 1):
        data = json.dumps({"sql": query})
        result = make_request(url, auth_base64, flags['timeout'], data=data, verbose=False)

        if result['success']:
            query_data = result['data']
            rows = query_data.get('row_count', 0)
            exec_time = query_data.get('execution_time_ms', 0)
            total_time += exec_time
            print(f"  ✅ Query {i}: {rows} rows ({exec_time:.1f}ms)")
        else:
            print(f"  ❌ Query {i} failed: {result['error']}")
            all_success = False

    print(f"  ⏱️  Total execution time: {total_time:.1f}ms")
    print()

    return {
        "success": all_success,
        "response_time_ms": total_time,
        "url": url
    }

def test_performance(flags: Dict[str, Any], auth_base64: str, verbose: bool) -> Dict[str, Any]:
    """Test database performance with multiple requests"""
    url = f"{flags['url']}/db/health"
    num_requests = 5
    times = []

    print(f"  🚀 Running {num_requests} concurrent health checks...")

    for i in range(num_requests):
        result = make_request(url, auth_base64, flags['timeout'], verbose=False)
        if result['success']:
            times.append(result['response_time_ms'])
        else:
            print(f"  ❌ Request {i+1} failed")
            return {
                "success": False,
                "response_time_ms": 0,
                "url": url
            }

    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"  ✅ Avg: {avg_time:.1f}ms, Min: {min_time:.1f}ms, Max: {max_time:.1f}ms")

        return {
            "success": True,
            "response_time_ms": avg_time,
            "url": url
        }

    print()
    return {
        "success": False,
        "response_time_ms": 0,
        "url": url
    }