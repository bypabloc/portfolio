# Atlas Tests: issuers
# Generado: 2025-09-23T22:04:32.013940

# Test 1: Verificar que la tabla existe
test "schema" "issuers_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'issuers';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "issuers_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'issuers';"
    output = "7"
  }
}

# Test 3: Verificar integridad de datos
test "data" "issuers_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM issuers;"
    output = "2"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM issuers WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM issuers WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
