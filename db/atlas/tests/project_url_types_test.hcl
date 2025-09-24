# Atlas Tests: project_url_types
# Generado: 2025-09-23T22:04:32.014102

# Test 1: Verificar que la tabla existe
test "schema" "project_url_types_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'project_url_types';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "project_url_types_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'project_url_types';"
    output = "7"
  }
}

# Test 3: Verificar integridad de datos
test "data" "project_url_types_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM project_url_types;"
    output = "2"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM project_url_types WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM project_url_types WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
