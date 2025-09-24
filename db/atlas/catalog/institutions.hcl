# Catalog: institutions
# Generado: 2025-09-23T22:04:31.827780

table "institutions" {
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

  column "url" {
    type = text
    null = false
  }

  column "location_url" {
    type = text
    null = true
  }

  column "map_embed" {
    type = text
    null = true
  }

  primary_key {
    columns = [column.id]
  }

  index "idx_institutions_code_name" {
    columns = [column.code_name]
    unique = true
  }
}
