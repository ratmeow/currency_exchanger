PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS currencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR,
    full_name VARCHAR,
    sign VARCHAR
);

CREATE UNIQUE INDEX IF NOT EXISTS code_idx ON currencies(code);

CREATE TABLE IF NOT EXISTS exchange_rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_currency_id INTEGER,
    target_currency_id INTEGER,
    rate DECIMAL(6),
    FOREIGN KEY(base_currency_id) REFERENCES currencies(id),
    FOREIGN KEY(target_currency_id) REFERENCES currencies(id)
);

CREATE UNIQUE INDEX IF NOT EXISTS base_target_idx ON exchange_rates(base_currency_id, target_currency_id);

INSERT INTO currencies (code, full_name, sign) VALUES
    ('USD', 'United States Dollar', '$'),
    ('EUR', 'Euro', '€'),
    ('JPY', 'Japanese Yen', '¥'),
    ('GBP', 'British Pound', '£'),
    ('AUD', 'Australian Dollar', 'A$'),
    ('CAD', 'Canadian Dollar', 'C$'),
    ('CHF', 'Swiss Franc', 'CHF'),
    ('CNY', 'Chinese Yuan', '¥'),
    ('SEK', 'Swedish Krona', 'kr'),
    ('NZD', 'New Zealand Dollar', 'NZ$');

INSERT INTO exchange_rates (base_currency_id, target_currency_id, rate) VALUES
    ((SELECT id FROM currencies WHERE code = 'USD'), (SELECT id FROM currencies WHERE code = 'EUR'), 0.92),
    ((SELECT id FROM currencies WHERE code = 'USD'), (SELECT id FROM currencies WHERE code = 'JPY'), 136.50),
    ((SELECT id FROM currencies WHERE code = 'USD'), (SELECT id FROM currencies WHERE code = 'GBP'), 0.77),
    ((SELECT id FROM currencies WHERE code = 'USD'), (SELECT id FROM currencies WHERE code = 'AUD'), 1.47),
    ((SELECT id FROM currencies WHERE code = 'EUR'), (SELECT id FROM currencies WHERE code = 'USD'), 1.09),
    ((SELECT id FROM currencies WHERE code = 'EUR'), (SELECT id FROM currencies WHERE code = 'JPY'), 148.12),
    ((SELECT id FROM currencies WHERE code = 'EUR'), (SELECT id FROM currencies WHERE code = 'GBP'), 0.84),
    ((SELECT id FROM currencies WHERE code = 'EUR'), (SELECT id FROM currencies WHERE code = 'AUD'), 1.60),
    ((SELECT id FROM currencies WHERE code = 'JPY'), (SELECT id FROM currencies WHERE code = 'USD'), 0.0073),
    ((SELECT id FROM currencies WHERE code = 'JPY'), (SELECT id FROM currencies WHERE code = 'EUR'), 0.0068),
    ((SELECT id FROM currencies WHERE code = 'GBP'), (SELECT id FROM currencies WHERE code = 'USD'), 1.30),
    ((SELECT id FROM currencies WHERE code = 'GBP'), (SELECT id FROM currencies WHERE code = 'EUR'), 1.18);
