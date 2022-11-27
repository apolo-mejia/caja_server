DROP TABLE IF EXISTS machines;

CREATE TABLE machines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- Reference fields
    name TEXT NOT NULL NOT NULL,
    id_process INTEGER NOT NULL,
    id_maintenance INTEGER NOT NULL,
    users TEXT NOT NULL,
-- Optional reference values
    brand TEXT,
    model TEXT,
    m_serial TEXT,
    i_serial TEXT,
-- Nominal values 
    kw_nom REAL NOT NULL,
    rpm_nom INTEGER NOT NULL,
-- Optinal nominal values
    i_nom INTEGER,
    v_nom INTEGER,
    n_phases INTEGER,
    n_poles INTEGER,
    f_nom INTEGER,
    nema_class INTEGER,
    ip_class INTEGER,
    housing INTEGER,
--Description
    a_status INTEGER NOT NULL,
    picture TEXT,
    avatar TEXT,
    description TEXT
);
