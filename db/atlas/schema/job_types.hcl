# Schema: job_types
# Generado: 2025-09-23T22:04:31.827452

table "job_types" {
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

  column "code_name" {
    type = text
    null = false
  }

  column "name" {
    type = text
    null = false
  }

  primary_key {
    columns = [column.id]
  }

  index "idx_job_types_code_name" {
    columns = [column.code_name]
    unique = true
  }
}
