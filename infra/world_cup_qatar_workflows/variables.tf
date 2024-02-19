variable "project_id" {
  description = "Project ID, used to enforce providing a project id."
  type        = string
}

variable "location" {
  description = "Location."
  type        = string
}

variable "workflow_name" {
  description = "Workflow name."
  type        = string
}

variable "workflow_sa" {
  description = "Workflow Service Account."
  type        = string
}