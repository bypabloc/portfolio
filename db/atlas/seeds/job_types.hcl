# Atlas Seed: job_types
# Generado: 2025-09-23T22:04:31.825604
# Total filas: 6

plan "seed_job_types" {
  migration = <<-SQL
    -- Seeds para tabla job_types
    INSERT INTO job_types (id, status, created_at, updated_at, code_name, name) VALUES
    ('6dddb9b2-3a8f-450c-8af8-77af61b63467', 'active', '2024-11-05 03:44:10', NULL, 'fullTime', 'Full Time'),
    ('4ac014f2-5a28-4614-a5e1-fd061917d0e7', 'active', '2024-11-05 03:44:10', NULL, 'partTime', 'Part Time'),
    ('2e11bfd7-06f0-4496-a5a1-50885ebf8548', 'active', '2024-11-05 03:44:10', NULL, 'freelance', 'Freelance'),
    ('4890e3fc-dfdc-4dd2-bd63-ef98f7029b16', 'active', '2024-11-05 03:44:10', NULL, 'internship', 'Internship'),
    ('d86edf33-c07e-40ee-9734-659f2588c626', 'active', '2024-11-05 03:44:10', NULL, 'contract', 'Contract'),
    ('f1a9d295-3591-4b3f-b11b-30dfd04be9b9', 'active', '2024-11-05 03:44:10', NULL, 'personalProject', 'Personal Project');
  SQL
}

locals {
  job_types_columns = ['id', 'status', 'created_at', 'updated_at', 'code_name', 'name']
  job_types_row_count = 6
}

# Test básico para validar la tabla
test "schema" "job_types_exists" {
  exec {
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'job_types';"
    output = "1"
  }
}
