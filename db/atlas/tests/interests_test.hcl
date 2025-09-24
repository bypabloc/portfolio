# Atlas Tests: interests
# Generado: 2025-09-23T22:04:32.013913

# Test 1: Verificar que la tabla existe
test "schema" "interests_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'interests';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "interests_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'interests';"
    output = "6"
  }
}

# Test 3: Verificar integridad de datos
test "data" "interests_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM interests;"
    output = "20"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM interests WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM interests WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
