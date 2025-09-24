# Atlas Tests: translations
# Generado: 2025-09-23T22:04:32.014302

# Test 1: Verificar que la tabla existe
test "schema" "translations_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'translations';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "translations_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'translations';"
    output = "9"
  }
}

# Test 3: Verificar integridad de datos
test "data" "translations_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM translations;"
    output = "542"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM translations WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM translations WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
