
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
INSERT INTO types VALUES ('box', 'box');
INSERT INTO types VALUES ('sphere', 'sphere');
INSERT INTO types VALUES ('torus', 'torus');
INSERT INTO types VALUES ('icosahedron', 'icosahedron');
INSERT INTO types VALUES ('textmd', 'textmd');
INSERT INTO types VALUES ('image_plane', 'image_plane');
INSERT INTO types VALUES ('spaceship', 'spaceship');
INSERT INTO types VALUES ('vague', 'vague');
INSERT INTO types VALUES ('nissangame', 'nissangame');
INSERT INTO types VALUES ('bibigame', 'bibigame');
