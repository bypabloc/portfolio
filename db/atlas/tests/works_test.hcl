# Atlas Tests: works
# Generado: 2025-09-23T22:04:32.014224

# Test 1: Verificar que la tabla existe
test "schema" "works_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'works';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "works_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'works';"
    output = "15"
  }
}

# Test 3: Verificar integridad de datos
test "data" "works_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM works;"
    output = "10"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM works WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM works WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
