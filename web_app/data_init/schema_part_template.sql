DROP TABLE IF EXISTS parts_templates;

CREATE TABLE parts_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--Reference fields
    name TEXT NOT NULL NOT NULL,
    type TEXT NOT NULL,
    users TEXT NOT NULL,
    categories TEXT,
--Optional reference values
    brand TEXT,
    model TEXT,
    m_serial TEXT,
--Description
    picture TEXT,
    avatar TEXT,
    description TEXT,
--Specific fields
    s_fields TEXT
);
