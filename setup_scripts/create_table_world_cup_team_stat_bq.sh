bq mk -t \
  --schema setup_scripts/schema/world_cup_team_player_stat_schema.json \
  --time_partitioning_field ingestionDate \
  --time_partitioning_type DAY \
  gb-poc-373711:qatar_fifa_world_cup.world_cup_team_players_stat