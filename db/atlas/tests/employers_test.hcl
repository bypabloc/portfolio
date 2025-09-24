# Atlas Tests: employers
# Generado: 2025-09-23T22:04:32.013880

# Test 1: Verificar que la tabla existe
test "schema" "employers_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'employers';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "employers_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'employers';"
    output = "10"
  }
}

# Test 3: Verificar integridad de datos
test "data" "employers_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM employers;"
    output = "8"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM employers WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM employers WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
