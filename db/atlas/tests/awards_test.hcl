# Atlas Tests: awards
# Generado: 2025-09-23T22:04:32.013759

# Test 1: Verificar que la tabla existe
test "schema" "awards_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'awards';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "awards_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'awards';"
    output = "11"
  }
}

# Test 3: Verificar integridad de datos
test "data" "awards_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM awards;"
    output = "2"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM awards WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM awards WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
