# Atlas Tests: files
# Generado: 2025-09-23T22:04:32.013792

# Test 1: Verificar que la tabla existe
test "schema" "files_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'files';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "files_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'files';"
    output = "10"
  }
}

# Test 3: Verificar integridad de datos
test "data" "files_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM files;"
    output = "8"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM files WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM files WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
