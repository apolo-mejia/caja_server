DROP TABLE IF EXISTS sensor_templates;

CREATE TABLE sensor_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--Reference fields,
    model TEXT,
--Description
    capacities TEXT,
    picture TEXT,
    avatar TEXT,
    description TEXT,
--Specific fields
    s_fields TEXT
);
