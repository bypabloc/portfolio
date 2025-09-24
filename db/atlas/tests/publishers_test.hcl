# Atlas Tests: publishers
# Generado: 2025-09-23T22:04:32.014131

# Test 1: Verificar que la tabla existe
test "schema" "publishers_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'publishers';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "publishers_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'publishers';"
    output = "7"
  }
}

# Test 3: Verificar integridad de datos
test "data" "publishers_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM publishers;"
    output = "1"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM publishers WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM publishers WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
