# Catalog: references
# Generado: 2025-09-23T22:04:31.827896

table "references" {
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

  column "reference" {
    type = text
    null = false
    comment = "Nombre de la persona que da la referencia"
  }

  column "position" {
    type = text
    null = false
  }

  column "url" {
    type = text
    null = false
  }

  column "employer_id" {
    type = text
    null = true
  }

  column "scrapping_recommendation" {
    type = text
    null = true
    comment = "Recomendación obtenida por scraping"
  }

  primary_key {
    columns = [column.id]
  }

  foreign_key "fk_references_user" {
    columns = [column.user_id]
    ref_columns = [table.users.column.id]
    on_delete = CASCADE
    on_update = RESTRICT
  }

  foreign_key "fk_references_employer" {
    columns = [column.employer_id]
    ref_columns = [table.employers.column.id]
    on_delete = SET_NULL
    on_update = RESTRICT
  }

  index "idx_references_user" {
    columns = [column.user_id]
  }
}
