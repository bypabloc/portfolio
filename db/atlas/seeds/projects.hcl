# Atlas Seed: projects
# Generado: 2025-09-23T22:04:31.825790
# Total filas: 3

plan "seed_projects" {
  migration = <<-SQL
    -- Seeds para tabla projects
    INSERT INTO projects (id, status, created_at, updated_at, user_id, code_name, name, description, highlights, url, service_status) VALUES
    ('9f250fe0-e7f9-4d46-824e-0f15a26e9727', 'active', '2024-11-05 03:44:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'extension-faststruct', 'FastStruct', 'Una extensión de VS Code para visualizar y documentar rápidamente la estructura de archivos de su proyecto. FastStruct le ayuda a crear documentación clara y bien formateada de la estructura de directorios de su proyecto, incluido el contenido de los archivos cuando sea necesario.', '["Solo por ocio aprender a hacer una extensión para VS Code y que me simplificara un proceso que tenia que hacer manual a la hora de interactuar con la IA."]', 'https://marketplace.visualstudio.com/items?itemName=the-full-stack.faststruct', 'active'),
    ('89d1383d-d26b-4402-9bc2-c2e7a04accf8', 'active', '2024-11-05 03:44:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'cv-bypabloc', 'Curriculum Vitae', 'Desarrollo de un currículum vitae en Astro para mostrar mis habilidades y experiencia laboral.', '["Practicar mis habilidades de desarrollo web con Astro","Mostrar mi experiencia laboral de forma clara y concisa"]', 'https://the-full-stack.com/', 'active'),
    ('6048cb58-383d-424f-9058-110ee554603d', 'active', '2024-11-05 03:44:42', NULL, 'c1819969-be87-420f-a7b3-31ad05001182', 'appinteli-bypabloc', 'ERP para pequeñas tiendas', 'Co-fundador y desarrollador de un ERP enfocado en la automatización de procesos de inventario, ventas y compras para pequeñas tiendas.', '["Desarrollo de una plataforma de comercio electrónico integrada","Gestión de cliente y proyecto desde cero"]', 'https://appinteli.com', 'inactive');
  SQL
}

locals {
  projects_columns = ['id', 'status', 'created_at', 'updated_at', 'user_id', 'code_name', 'name', 'description', 'highlights', 'url', 'service_status']
  projects_row_count = 3
}

# Test básico para validar la tabla
test "schema" "projects_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'projects';"
    output = "1"
  }
}
