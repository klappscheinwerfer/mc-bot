CREATE TABLE IF NOT EXISTS `setting` (
	setting_key TEXT PRIMARY KEY,
	setting_value TEXT
);

/*
CREATE TABLE IF NOT EXISTS `event` (
	event_id INTEGER PRIMARY KEY AUTOINCREMENT,
	event_type TEXT,
	event_text TEXT,
	event_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
*/
