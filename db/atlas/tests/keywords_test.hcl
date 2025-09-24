# Atlas Tests: keywords
# Generado: 2025-09-23T22:04:32.013976

# Test 1: Verificar que la tabla existe
test "schema" "keywords_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'keywords';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "keywords_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'keywords';"
    output = "7"
  }
}

# Test 3: Verificar integridad de datos
test "data" "keywords_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM keywords;"
    output = "69"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM keywords WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM keywords WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
