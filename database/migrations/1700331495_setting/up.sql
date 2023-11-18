CREATE TABLE IF NOT EXISTS `setting` (
	setting_key TEXT PRIMARY KEY,
	setting_value TEXT
);

INSERT INTO setting
	( setting_key, setting_value )
VALUES
	("db-version", "1700331495_setting"),
	("embed-color", "#40a45c"),
	("embed-error-color", "#e02b2b")