-- Сервис формирования списка подарков: реляционная схема ПР7.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS gift_lists (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recipients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS occasions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    event_date TEXT NOT NULL,
    recipient_id INTEGER NOT NULL,
    FOREIGN KEY (recipient_id) REFERENCES recipients(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS gifts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL CHECK (price > 0),
    purchased INTEGER NOT NULL DEFAULT 0 CHECK (purchased IN (0, 1)),
    gift_list_id INTEGER NOT NULL,
    occasion_id INTEGER NOT NULL,
    FOREIGN KEY (gift_list_id) REFERENCES gift_lists(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (occasion_id) REFERENCES occasions(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_occasions_recipient
    ON occasions(recipient_id);
CREATE INDEX IF NOT EXISTS idx_occasions_event_date
    ON occasions(event_date);
CREATE INDEX IF NOT EXISTS idx_gifts_occasion
    ON gifts(occasion_id);
CREATE INDEX IF NOT EXISTS idx_gifts_list
    ON gifts(gift_list_id);
CREATE INDEX IF NOT EXISTS idx_gifts_price
    ON gifts(price);
