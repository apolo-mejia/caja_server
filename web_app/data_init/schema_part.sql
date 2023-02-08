DROP TABLE IF EXISTS parts;

CREATE TABLE parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--Reference fields
    name TEXT NOT NULL NOT NULL,
    id_machine INTEGER NOT NULL,
    ordinal INTEGER NOT NULL,
    id_maintenance INTEGER NOT NULL,
    type TEXT NOT NULL,
    users TEXT NOT NULL,
    template INTEGER NOT NULL,
    c_task INTEGER NOT NULL,
--Optional reference values
    brand TEXT,
    model TEXT,
    m_serial TEXT,
    i_serial TEXT,
--Description
    a_status INTEGER NOT NULL,
    picture TEXT,
    avatar TEXT,
    description TEXT,
--Specific fields
    s_fields TEXT
);
