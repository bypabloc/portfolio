# Atlas Tests: projects
# Generado: 2025-09-23T22:04:32.014068

# Test 1: Verificar que la tabla existe
test "schema" "projects_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'projects';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "projects_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'projects';"
    output = "11"
  }
}

# Test 3: Verificar integridad de datos
test "data" "projects_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM projects;"
    output = "3"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM projects WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM projects WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
