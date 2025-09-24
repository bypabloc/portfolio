# Schema: projects
# Generado: 2025-09-23T22:04:31.827496

table "projects" {
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

  column "code_name" {
    type = text
    null = false
  }

  column "name" {
    type = text
    null = false
  }

  column "description" {
    type = text
    null = false
  }

  column "highlights" {
    type = text
    null = false
    comment = "Logros y características destacadas del proyecto"
  }

  column "url" {
    type = text
    null = false
  }

  column "service_status" {
    type = text
    null = false
    default = "active"
  }

  primary_key {
    columns = [column.id]
  }

  foreign_key "fk_projects_user" {
    columns = [column.user_id]
    ref_columns = [table.users.column.id]
    on_delete = CASCADE
    on_update = RESTRICT
  }

  index "idx_projects_user" {
    columns = [column.user_id]
  }

  index "idx_projects_code_name" {
    columns = [column.user_id, column.code_name]
    unique = true
  }

  index "idx_projects_service_status" {
    columns = [column.service_status]
  }
}
