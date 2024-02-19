locals {
  world_cup_qatar_functions_workflow_yaml_as_string   = file("${path.module}/resource/workflow/world_cup_qatar_functions_workflow.yaml")
  world_cup_qatar_functions_workflow_config_as_string = file("${path.module}/resource/workflow/config/workflow_config.json")
  world_cup_qatar_functions_workflow_config           = jsondecode(file("${path.module}/resource/workflow/config/workflow_config.json"))
}