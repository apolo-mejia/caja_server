DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--Reference fields
    name TEXT NOT NULL NOT NULL,
    id_machine INTEGER,
    id_part INTEGER NOT NULL,
    id_maintenance INTEGER NOT NULL,
    id_template INTEGER NOT NULL,
    c_task INTEGER NOT NULL,
--Measure values
    c_measure REAL,
    units TEXT NOT NULL,
--Schedule data
    d_start TEXT NOT NULL,
    d_end TEXT,
    d_allow INTEGER NOT NULL,
    t_interval INTEGER NOT NULL,
    hf_start TEXT,
    hf_end TEXT,
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
