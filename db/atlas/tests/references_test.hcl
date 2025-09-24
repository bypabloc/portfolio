# Atlas Tests: references
# Generado: 2025-09-23T22:04:32.014145

# Test 1: Verificar que la tabla existe
test "schema" "references_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'references';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "references_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'references';"
    output = "12"
  }
}

# Test 3: Verificar integridad de datos
test "data" "references_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM references;"
    output = "10"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM references WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM references WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
