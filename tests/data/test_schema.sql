PRAGMA foreign_keys = ON;

DROP INDEX IF EXISTS code_idx;
DROP INDEX IF EXISTS base_target_idx;
DROP TABLE IF EXISTS exchange_rates;
DROP TABLE IF EXISTS currencies;


CREATE TABLE currencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR,
    full_name VARCHAR,
    sign VARCHAR
);

CREATE UNIQUE INDEX code_idx ON currencies(code);

CREATE TABLE exchange_rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_currency_id INTEGER,
    target_currency_id INTEGER,
    rate DECIMAL(6),
    FOREIGN KEY(base_currency_id) REFERENCES currencies(id),
    FOREIGN KEY(target_currency_id) REFERENCES currencies(id)
);

CREATE UNIQUE INDEX base_target_idx ON exchange_rates(base_currency_id, target_currency_id);

INSERT INTO currencies (code, full_name, sign) VALUES
    ('USD', 'United States Dollar', '$'),
    ('EUR', 'Euro', '€'),
    ('JPY', 'Japanese Yen', '¥');

INSERT INTO exchange_rates (base_currency_id, target_currency_id, rate) VALUES
    ((SELECT id FROM currencies WHERE code = 'USD'), (SELECT id FROM currencies WHERE code = 'EUR'), 0.92),
    ((SELECT id FROM currencies WHERE code = 'USD'), (SELECT id FROM currencies WHERE code = 'JPY'), 136.50),
    ((SELECT id FROM currencies WHERE code = 'EUR'), (SELECT id FROM currencies WHERE code = 'USD'), 1.09),
    ((SELECT id FROM currencies WHERE code = 'EUR'), (SELECT id FROM currencies WHERE code = 'JPY'), 148.12),
    ((SELECT id FROM currencies WHERE code = 'JPY'), (SELECT id FROM currencies WHERE code = 'USD'), 0.0073),
    ((SELECT id FROM currencies WHERE code = 'JPY'), (SELECT id FROM currencies WHERE code = 'EUR'), 0.0068)
