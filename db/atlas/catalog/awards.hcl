# Catalog: awards
# Generado: 2025-09-23T22:04:31.827854

table "awards" {
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

  column "title" {
    type = text
    null = false
  }

  column "date" {
    type = date
    null = false
  }

  column "awarder" {
    type = text
    null = false
    comment = "Organización que otorga el premio"
  }

  column "summary" {
    type = text
    null = false
  }

  column "url" {
    type = text
    null = false
  }

  primary_key {
    columns = [column.id]
  }

  foreign_key "fk_awards_user" {
    columns = [column.user_id]
    ref_columns = [table.users.column.id]
    on_delete = CASCADE
    on_update = RESTRICT
  }

  index "idx_awards_user" {
    columns = [column.user_id]
  }

  index "idx_awards_date" {
    columns = [column.date]
  }
}
