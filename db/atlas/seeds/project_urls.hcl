# Atlas Seed: project_urls
# Generado: 2025-09-23T22:04:31.825815
# Total filas: 4

plan "seed_project_urls" {
  migration = <<-SQL
    -- Seeds para tabla project_urls
    INSERT INTO project_urls (id, status, created_at, updated_at, project_id, url_type_id, url) VALUES
    ('a2fdc434-0406-4577-a398-2702fe9d0aef', 'active', '2024-11-05 03:51:11', NULL, '89d1383d-d26b-4402-9bc2-c2e7a04accf8', '1b44fc21-afc2-4dbc-98c9-47f58a21c236', 'https://github.com/bypabloc/cv'),
    ('ce49151c-ecc6-489d-98f3-92aaae778ac0', 'active', '2024-11-05 03:51:11', NULL, '9f250fe0-e7f9-4d46-824e-0f15a26e9727', '1b44fc21-afc2-4dbc-98c9-47f58a21c236', 'https://github.com/bypabloc/faststruct'),
    ('03e9bfdb-f3f0-4ce0-8c21-ca1d76f94580', 'active', '2024-11-05 03:51:11', NULL, '9f250fe0-e7f9-4d46-824e-0f15a26e9727', '167cab5e-56e8-4275-a48b-4d47dc5a3f38', 'https://marketplace.visualstudio.com/items?itemName=the-full-stack.faststruct'),
    ('cc3cfe2a-d268-4ae0-87b2-a550d8e80921', 'active', '2024-11-05 03:51:11', NULL, '89d1383d-d26b-4402-9bc2-c2e7a04accf8', '167cab5e-56e8-4275-a48b-4d47dc5a3f38', 'https://pablocodes.com');
  SQL
}

locals {
  project_urls_columns = ['id', 'status', 'created_at', 'updated_at', 'project_id', 'url_type_id', 'url']
  project_urls_row_count = 4
}

# Test básico para validar la tabla
test "schema" "project_urls_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'project_urls';"
    output = "1"
  }
}
