# Atlas Seed: networks
# Generado: 2025-09-23T22:04:31.825744
# Total filas: 5

plan "seed_networks" {
  migration = <<-SQL
    -- Seeds para tabla networks
    INSERT INTO networks (id, status, created_at, updated_at, code_name, name, url, config) VALUES
    ('9c3b5049-aba3-48b3-b858-0a372f9af9cf', 'active', '2024-11-05 03:44:03', NULL, 'phone', 'Teléfono', 'tel', '{"description":"Comunicarse con {attributes.names.value} {attributes.lastName.value} a través de {name}","icon":{"default":"i-material-symbols-phone-enabled-outline","dark":"i-material-symbols-phone-enabled"},"web":{"visible":true,"template":"{url}:{contactInfo}"},"print":{"visible":false,"template":"{contactInfo}"}}'),
    ('21f0ebb7-5fe0-4382-8129-5e8a82ccbbaf', 'active', '2024-11-05 03:44:03', NULL, 'email', 'Correo Electrónico', 'mailto', '{"description":"Comunicarse con {attributes.names.value} {attributes.lastName.value} a través del {name}","icon":{"default":"i-material-symbols-mail-outline","dark":"i-material-symbols-mail"},"web":{"visible":true,"template":"{url}:{contactInfo}"},"print":{"visible":true,"template":"{contactInfo}"}}'),
    ('253010e7-1b55-409a-bd52-6c4efd112692', 'active', '2024-11-05 03:44:03', NULL, 'whatsapp', 'WhatsApp', 'https://wa.me', '{"icon":{"default":"i-mdi-whatsapp","dark":"i-mdi-whatsapp"},"description":"Comunicarse con {attributes.names.value} {attributes.lastName.value} a través {name}","web":{"visible":true,"template":"{url}/{contactInfo}"},"print":{"visible":true,"template":"+{contactInfo}"}}'),
    ('43e96f18-dca5-474e-9bf9-5db43e73400d', 'active', '2024-11-05 03:44:03', NULL, 'linkedin', 'LinkedIn', 'https://linkedin.com/in', '{"description":"Visitar el perfil de {attributes.names.value} {attributes.lastName.value} en {name}","icon":{"default":"i-ant-design-linkedin-outlined","dark":"i-ant-design-linkedin-filled"},"web":{"visible":true,"template":"{url}/{contactInfo}"},"print":{"visible":true,"link":true,"template":"{url}/{contactInfo}"}}'),
    ('915a7d0f-236f-4ba7-9741-15111cfb0c6c', 'active', '2024-11-05 03:44:03', NULL, 'github', 'GitHub', 'https://github.com', '{"description":"Visitar el perfil de {attributes.names.value} {attributes.lastName.value} en {name}","icon":{"default":"i-ant-design-github-outlined","dark":"i-ant-design-github-filled"},"web":{"visible":true,"template":"{url}/{contactInfo}"},"print":{"visible":true,"link":true,"template":"{url}/{contactInfo}"}}');
  SQL
}

locals {
  networks_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name', 'url', 'config']
  networks_row_count = 5
}

# Test básico para validar la tabla
test "schema" "networks_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'networks';"
    output = "1"
  }
}
