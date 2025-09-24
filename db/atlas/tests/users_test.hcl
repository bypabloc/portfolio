# Atlas Tests: users
# Generado: 2025-09-23T22:04:32.013582

# Test 1: Verificar que la tabla existe
test "schema" "users_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'users';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "users_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'users';"
    output = "5"
  }
}

# Test 3: Verificar integridad de datos
test "data" "users_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM users;"
    output = "1"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM users WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM users WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
