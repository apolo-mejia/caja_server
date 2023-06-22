DROP TABLE IF EXISTS sensors;

CREATE TABLE sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--Reference fields,
    part_id INTEGER,
    model TEXT,
    alias TEXT,
    mac TEXT,
--Description
    capacities TEXT,
    picture TEXT,
    avatar TEXT,
    description TEXT,
--Specific fields
    s_fields TEXT
);
