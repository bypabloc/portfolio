# Atlas Tests: institutions
# Generado: 2025-09-23T22:04:32.013897

# Test 1: Verificar que la tabla existe
test "schema" "institutions_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'institutions';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "institutions_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'institutions';"
    output = "9"
  }
}

# Test 3: Verificar integridad de datos
test "data" "institutions_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM institutions;"
    output = "3"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM institutions WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM institutions WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
