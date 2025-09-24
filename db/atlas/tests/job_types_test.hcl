# Atlas Tests: job_types
# Generado: 2025-09-23T22:04:32.013960

# Test 1: Verificar que la tabla existe
test "schema" "job_types_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'job_types';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "job_types_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'job_types';"
    output = "6"
  }
}

# Test 3: Verificar integridad de datos
test "data" "job_types_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM job_types;"
    output = "6"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM job_types WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM job_types WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
