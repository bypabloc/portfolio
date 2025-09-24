# Atlas Tests: networks_users
# Generado: 2025-09-23T22:04:32.014044

# Test 1: Verificar que la tabla existe
test "schema" "networks_users_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'networks_users';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "networks_users_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'networks_users';"
    output = "8"
  }
}

# Test 3: Verificar integridad de datos
test "data" "networks_users_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM networks_users;"
    output = "5"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM networks_users WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM networks_users WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
