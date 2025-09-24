# Atlas Tests: works_technical_skills
# Generado: 2025-09-23T22:04:32.014275

# Test 1: Verificar que la tabla existe
test "schema" "works_technical_skills_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'works_technical_skills';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "works_technical_skills_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'works_technical_skills';"
    output = "6"
  }
}

# Test 3: Verificar integridad de datos
test "data" "works_technical_skills_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM works_technical_skills;"
    output = "50"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM works_technical_skills WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM works_technical_skills WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
