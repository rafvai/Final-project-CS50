


SELECT name, set_up, action, return, starting_position, pattern, link FROM exercises JOIN players ON exercises.name = players.exercise WHERE users_id = 5;