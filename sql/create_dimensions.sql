-- Customers table

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL
);

-- Agents table

CREATE TABLE IF NOT EXISTS agents (
    agent_id TEXT PRIMARY KEY,
    agent_name TEXT NOT NULL
);

-- Insert customers

INSERT OR IGNORE INTO customers (
    customer_id,
    customer_name
)
SELECT DISTINCT
    customer_id,
    'Customer ' || SUBSTR(customer_id, 2)
FROM tickets;

-- Insert agents

INSERT OR IGNORE INTO agents (
    agent_id,
    agent_name
)
SELECT DISTINCT
    agent_id,
    'Agent ' || SUBSTR(agent_id, 2)
FROM tickets;