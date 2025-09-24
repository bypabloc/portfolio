# Atlas Tests: interests_keywords
# Generado: 2025-09-23T22:04:32.014289

# Test 1: Verificar que la tabla existe
test "schema" "interests_keywords_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'interests_keywords';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "interests_keywords_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'interests_keywords';"
    output = "6"
  }
}

# Test 3: Verificar integridad de datos
test "data" "interests_keywords_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM interests_keywords;"
    output = "21"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM interests_keywords WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM interests_keywords WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
