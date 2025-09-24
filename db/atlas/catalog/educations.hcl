# Catalog: educations
# Generado: 2025-09-23T22:04:31.827802

table "educations" {
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

  column "institution_id" {
    type = text
    null = false
  }

  column "code_name" {
    type = text
    null = false
  }

  column "area" {
    type = text
    null = false
  }

  column "learn" {
    type = text
    null = false
    comment = "Título o programa de estudio"
  }

  column "study_type" {
    type = text
    null = false
    comment = "Carrera, Master, Diplomado, etc."
  }

  column "start_date" {
    type = date
    null = false
  }

  column "end_date" {
    type = date
    null = true
  }

  primary_key {
    columns = [column.id]
  }

  foreign_key "fk_educations_user" {
    columns = [column.user_id]
    ref_columns = [table.users.column.id]
    on_delete = CASCADE
    on_update = RESTRICT
  }

  foreign_key "fk_educations_institution" {
    columns = [column.institution_id]
    ref_columns = [table.institutions.column.id]
    on_delete = RESTRICT
    on_update = RESTRICT
  }

  index "idx_educations_user" {
    columns = [column.user_id]
  }

  index "idx_educations_dates" {
    columns = [column.start_date, column.end_date]
  }
}
