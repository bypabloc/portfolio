# Atlas Tests: languages_users
# Generado: 2025-09-23T22:04:32.014006

# Test 1: Verificar que la tabla existe
test "schema" "languages_users_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'languages_users';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "languages_users_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'languages_users';"
    output = "8"
  }
}

# Test 3: Verificar integridad de datos
test "data" "languages_users_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM languages_users;"
    output = "2"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM languages_users WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM languages_users WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
