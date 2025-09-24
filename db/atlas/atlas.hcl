# Atlas Configuration - Portfolio Database Schema
# Configuración principal de Atlas para el sistema de portfolio

# Variables de entorno para conexión a la base de datos
variable "database_url" {
  type        = string
  description = "Database connection string"
  default     = env("DATABASE_URL")
}

# Configuración del entorno
env "local" {
  src = [
    "schema.hcl",
    "catalog.hcl",
    "relationships.hcl"
  ]

  url = var.database_url

  dev = "docker://postgres/17/dev?search_path=public"

  # Configuración de migración
  migration {
    dir = "file://migrations"
  }

  # Configuración de formato
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}

env "development" {
  src = [
    "schema.hcl",
    "catalog.hcl",
    "relationships.hcl"
  ]

  url = var.database_url

  migration {
    dir = "file://migrations"
  }
}

env "staging" {
  src = [
    "schema.hcl",
    "catalog.hcl",
    "relationships.hcl"
  ]

  url = var.database_url

  migration {
    dir = "file://migrations"
  }
}

env "production" {
  src = [
    "schema.hcl",
    "catalog.hcl",
    "relationships.hcl"
  ]

  url = var.database_url

  migration {
    dir = "file://migrations"
  }

  # Configuración de lint para producción
  lint {
    destructive {
      error = true
    }
  }
}