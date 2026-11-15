DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    customer_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT NOT NULL,
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    sla_deadline TEXT NOT NULL,
    status TEXT NOT NULL,
    reopened INTEGER NOT NULL
);