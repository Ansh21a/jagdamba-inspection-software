-- Jagdamba Inspection Software - SQLite Schema Backup
-- Use this as a reference/source-of-truth for table structure.
-- (Admin seed: admin/admin123)


CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE,
  password TEXT,
  role TEXT
);

CREATE TABLE IF NOT EXISTS party_master(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  party_name TEXT,
  address TEXT,
  gst_no TEXT
);

CREATE TABLE IF NOT EXISTS inspector_master(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  inspector_name TEXT,
  designation TEXT
);

CREATE TABLE IF NOT EXISTS reports(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  party TEXT,
  inspector TEXT,
  insp_date TEXT
);

INSERT OR IGNORE INTO users(username,password,role)
VALUES('admin','admin123','admin');

