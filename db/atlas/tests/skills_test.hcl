# Atlas Tests: skills
# Generado: 2025-09-23T22:04:32.014160

# Test 1: Verificar que la tabla existe
test "schema" "skills_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'skills';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "skills_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'skills';"
    output = "8"
  }
}

# Test 3: Verificar integridad de datos
test "data" "skills_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM skills;"
    output = "91"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM skills WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM skills WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
