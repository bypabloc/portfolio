# Schema: users
# Generado: 2025-09-23T22:04:31.827366

table "users" {
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

  column "username" {
    type = text
    null = false
  }

  primary_key {
    columns = [column.id]
  }

  index "idx_users_username" {
    columns = [column.username]
    unique = true
  }

  index "idx_users_status" {
    columns = [column.status]
  }
}
