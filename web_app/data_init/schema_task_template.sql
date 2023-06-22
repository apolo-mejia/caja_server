DROP TABLE IF EXISTS task_templates;

CREATE TABLE task_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--Reference fields
    name TEXT NOT NULL,
    capacities TEXT NOT NULL,
--Measure values
    units TEXT NOT NULL,
    site TEXT NOT NULL,
--Schedule data
    d_allow INTEGER NOT NULL,
    t_interval INTEGER NOT NULL,
--Alarm values
    s_val REAL NOT NULL,
    g_val REAL NOT NULL,
    y_val REAL NOT NULL,
    o_val REAL NOT NULL,
    r_val REAL NOT NULL,
--Specific fields
    s_fields TEXT,
    description TEXT,
    avatar TEXT,
    help TEXT
);
