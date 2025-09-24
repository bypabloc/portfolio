# Atlas Tests: networks
# Generado: 2025-09-23T22:04:32.014019

# Test 1: Verificar que la tabla existe
test "schema" "networks_table_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'networks';"
    output = "1"
  }
}

# Test 2: Verificar columnas esperadas
test "schema" "networks_columns_exist" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'networks';"
    output = "8"
  }
}

# Test 3: Verificar integridad de datos
test "data" "networks_data_integrity" {
  exec {
    sql = "SELECT COUNT(*) FROM networks;"
    output = "5"
  }

  # Test 4: Verificar primary key
  exec {
    sql = "SELECT COUNT(*) FROM networks WHERE id IS NULL;"
    output = "0"
  }

  # Test 5: Verificar valores de status
  exec {
    sql = "SELECT DISTINCT status FROM networks WHERE status NOT IN ('active', 'inactive', 'pending');"
  }
}
