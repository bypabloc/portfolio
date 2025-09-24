# Atlas Tests: educations
# Generado: 2025-09-23T22:04:32.013822

# Test 1: Verificar que la tabla existe
test "schema" "educations_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'educations';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "educations_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'educations';"
    output = "12"
  }
}

# Test 3: Verificar integridad de datos
test "data" "educations_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM educations;"
    output = "3"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM educations WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM educations WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
