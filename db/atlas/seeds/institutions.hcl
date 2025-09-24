# Atlas Seed: institutions
# Generado: 2025-09-23T22:04:31.825529
# Total filas: 3

plan "seed_institutions" {
  migration = <<-SQL
    -- Seeds para tabla institutions
    INSERT INTO institutions (id, status, created_at, updated_at, code_name, name, url, location_url, map_embed) VALUES
    ('03f6e5db-aeec-4cf4-83d6-46ffa1eb4083', 'active', '2024-11-05 03:44:05', NULL, 'uptyab', 'Universidad Politécnica Territorial de Yaracuy Arístides Bastidas (UPTYAB)', 'http://www.uptyab.edu.ve/web/index.php', 'https://maps.app.goo.gl/kKW1WfPh1YmCb495A', '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3925.130375903552!2d-68.75705208540283!3d10.3314499212098!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8e80c8d433543891%3A0x5d6f1945598c22ac!2sUniversidad%20Polit%C3%A9cnica%20Territorial%20de%20Yaracuy%20Ar%C3%ADstides%20Bastidas%20(UPTYAB)!5e0!3m2!1ses!2spe!4v1714485380993!5m2!1ses!2spe" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'),
    ('0c41d325-8545-43fb-b13d-bb4d83e59b2b', 'active', '2024-11-05 03:44:05', NULL, 'youtube', 'YouTube', 'https://youtube.com', NULL, NULL),
    ('ced3de3e-fc5a-46bf-a958-c7ca156f0c3c', 'active', '2024-11-05 03:44:05', NULL, 'udemy', 'Udemy', 'https://udemy.com', NULL, NULL);
  SQL
}

locals {
  institutions_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name', 'url', 'location_url', 'map_embed']
  institutions_row_count = 3
}

# Test básico para validar la tabla
test "schema" "institutions_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'institutions';"
    output = "1"
  }
}
