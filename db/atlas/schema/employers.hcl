# Schema: employers
# Generado: 2025-09-23T22:04:31.827435

table "employers" {
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
    null = true
    comment = "Usuario propietario del empleador (si es privado)"
  }

  column "code_name" {
    type = text
    null = false
  }

  column "name" {
    type = text
    null = false
  }

  column "url" {
    type = text
    null = true
  }

  column "description" {
    type = text
    null = true
  }

  column "service_status" {
    type = text
    null = false
    default = "active"
  }

  primary_key {
    columns = [column.id]
  }

  foreign_key "fk_employers_user" {
    columns = [column.user_id]
    ref_columns = [table.users.column.id]
    on_delete = CASCADE
    on_update = RESTRICT
  }

  index "idx_employers_code_name" {
    columns = [column.code_name]
    unique = true
  }

  index "idx_employers_name" {
    columns = [column.name]
  }
}
