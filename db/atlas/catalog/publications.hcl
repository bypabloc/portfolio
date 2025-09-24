# Catalog: publications
# Generado: 2025-09-23T22:04:31.827882

table "publications" {
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

  column "name" {
    type = text
    null = false
  }

  column "publisher_id" {
    type = text
    null = false
  }

  column "release_date" {
    type = date
    null = false
  }

  column "url" {
    type = text
    null = false
  }

  column "summary" {
    type = text
    null = false
  }

  primary_key {
    columns = [column.id]
  }

  foreign_key "fk_publications_user" {
    columns = [column.user_id]
    ref_columns = [table.users.column.id]
    on_delete = CASCADE
    on_update = RESTRICT
  }

  foreign_key "fk_publications_publisher" {
    columns = [column.publisher_id]
    ref_columns = [table.publishers.column.id]
    on_delete = RESTRICT
    on_update = RESTRICT
  }

  index "idx_publications_user" {
    columns = [column.user_id]
  }

  index "idx_publications_date" {
    columns = [column.release_date]
  }
}
