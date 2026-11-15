-- QUERY 1: Tickets by status

SELECT
    status,
    COUNT(*) AS total_tickets
FROM tickets
GROUP BY status
ORDER BY total_tickets DESC;


-- QUERY 2: Tickets by category

SELECT
    category,
    COUNT(*) AS total_tickets
FROM tickets
GROUP BY category
ORDER BY total_tickets DESC;


-- QUERY 3: Performance by priority

SELECT
    priority,
    COUNT(*) AS resolved_tickets,

    ROUND(
        AVG(
            (julianday(resolved_at) - julianday(created_at)) * 24
        ), 2
    ) AS avg_resolution_hours,

    ROUND(
        AVG(
            CASE
                WHEN resolved_at <= sla_deadline THEN 1.0
                ELSE 0.0
            END
        ) * 100, 2
    ) AS sla_compliance_pct

FROM tickets

WHERE status = 'Resolved'

GROUP BY priority

ORDER BY
    CASE priority
        WHEN 'Urgent' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        ELSE 4
    END;

    -- QUERY 4: Top 10 customers

SELECT
    c.customer_id,
    c.customer_name,
    COUNT(t.ticket_id) AS total_tickets

FROM customers c

JOIN tickets t
    ON c.customer_id = t.customer_id

GROUP BY
    c.customer_id,
    c.customer_name

ORDER BY total_tickets DESC

LIMIT 10;


-- QUERY 5: Workload by agent

SELECT
    a.agent_id,
    a.agent_name,
    COUNT(t.ticket_id) AS assigned_tickets

FROM agents a

JOIN tickets t
    ON a.agent_id = t.agent_id

GROUP BY
    a.agent_id,
    a.agent_name

ORDER BY assigned_tickets DESC;

-- QUERY 6: Customer concentration analysis

WITH customer_tickets AS (

    SELECT
        customer_id,
        COUNT(*) AS total_tickets

    FROM tickets

    GROUP BY customer_id

),

top_customers AS (

    SELECT
        customer_id,
        total_tickets

    FROM customer_tickets

    ORDER BY total_tickets DESC

    LIMIT 8

)

SELECT
    COUNT(*) AS top_customers_count,

    SUM(total_tickets) AS tickets_from_top_customers,

    (SELECT COUNT(*) FROM tickets) AS all_tickets,

    ROUND(
        100.0 * SUM(total_tickets)
        / (SELECT COUNT(*) FROM tickets),
        2
    ) AS ticket_share_percentage

FROM top_customers;