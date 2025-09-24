# Schema: users_attributes
# Generado: 2025-09-23T22:04:31.827408

table "users_attributes" {
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
    comment = "Identificador único del atributo para este usuario"
  }

  column "user_id" {
    type = text
    null = false
  }

  column "attribute_type_id" {
    type = text
    null = false
  }

  column "attribute_value" {
    type = text
    null = false
    comment = "Valor del atributo (JSON para objetos complejos)"
  }

  primary_key {
    columns = [column.id]
  }

  foreign_key "fk_users_attributes_user" {
    columns = [column.user_id]
    ref_columns = [table.users.column.id]
    on_delete = CASCADE
    on_update = RESTRICT
  }

  foreign_key "fk_users_attributes_type" {
    columns = [column.attribute_type_id]
    ref_columns = [table.attributes_types.column.id]
    on_delete = RESTRICT
    on_update = RESTRICT
  }

  index "idx_users_attributes_user" {
    columns = [column.user_id]
  }

  index "idx_users_attributes_code_name" {
    columns = [column.user_id, column.code_name]
    unique = true
  }
}
