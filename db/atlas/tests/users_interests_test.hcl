# Atlas Tests: users_interests
# Generado: 2025-09-23T22:04:32.014175

# Test 1: Verificar que la tabla existe
test "schema" "users_interests_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'users_interests';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "users_interests_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'users_interests';"
    output = "6"
  }
}

# Test 3: Verificar integridad de datos
test "data" "users_interests_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM users_interests;"
    output = "20"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM users_interests WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM users_interests WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
