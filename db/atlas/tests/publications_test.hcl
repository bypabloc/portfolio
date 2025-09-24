# Atlas Tests: publications
# Generado: 2025-09-23T22:04:32.014116

# Test 1: Verificar que la tabla existe
test "schema" "publications_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'publications';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "publications_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'publications';"
    output = "10"
  }
}

# Test 3: Verificar integridad de datos
test "data" "publications_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM publications;"
    output = "5"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM publications WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM publications WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
