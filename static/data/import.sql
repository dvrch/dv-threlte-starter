
CREATE TABLE types (id TEXT PRIMARY KEY, name TEXT);
CREATE TABLE geometries (
    id TEXT PRIMARY KEY,
    name TEXT,
    type TEXT,
    color TEXT,
    position_x REAL, position_y REAL, position_z REAL,
    rotation_x REAL, rotation_y REAL, rotation_z REAL,
    scale_x REAL, scale_y REAL, scale_z REAL,
    visible INTEGER,
    model_url TEXT
);
