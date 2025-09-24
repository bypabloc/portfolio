# Schema: works
# Generado: 2025-09-23T22:04:31.827467

table "works" {
schema = schema.portfolio

  column "id" {
    type = text
    null = false
    default = sql("gen_random_uuid()::text")
  }

  column "status" {
    type = text
    null = false
    default = "active"
  }

  column "created_at" {
    type = timestamptz
    null = false
    default = sql("CURRENT_TIMESTAMP")
  }

  column "updated_at" {
    type = timestamptz
    null = true
  }

  column "user_id" {
    type = text
    null = false
  }

  column "employer_id" {
    type = text
    null = true
  }

  column "code_name" {
    type = text
    null = false
  }

  column "name" {
    type = text
    null = false
    comment = "Nombre del puesto/posición"
  }

  column "position" {
    type = text
    null = false
  }

  column "start_date" {
    type = date
    null = false
  }

  column "end_date" {
    type = date
    null = true
  }

  column "job_type_id" {
    type = text
    null = false
  }

  column "summary" {
    type = text
    null = true
  }

  column "responsibilities_n_projects" {
    type = text
    null = true
    comment = "Responsabilidades y proyectos realizados"
  }

  column "achievements" {
    type = text
    null = true
  }

  primary_key {
    columns = [column.id]
  }

  foreign_key "fk_works_user" {
    columns = [column.user_id]
    ref_columns = [table.users.column.id]
    on_delete = CASCADE
    on_update = RESTRICT
  }

  foreign_key "fk_works_employer" {
    columns = [column.employer_id]
    ref_columns = [table.employers.column.id]
    on_delete = SET_NULL
    on_update = RESTRICT
  }

  foreign_key "fk_works_job_type" {
    columns = [column.job_type_id]
    ref_columns = [table.job_types.column.id]
    on_delete = RESTRICT
    on_update = RESTRICT
  }

  index "idx_works_user" {
    columns = [column.user_id]
  }

  index "idx_works_dates" {
    columns = [column.start_date, column.end_date]
  }

  index "idx_works_code_name" {
    columns = [column.user_id, column.code_name]
    unique = true
  }
}
