SET timezone = 'America/Sao_Paulo';

CREATE TABLE IF NOT EXISTS customers
(
    id            INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name          VARCHAR(50) UNIQUE NOT NULL,
    balance       INTEGER            NOT NULL DEFAULT 0,
    account_limit INTEGER            NOT NULL
);

INSERT INTO customers (name, account_limit)
VALUES ('Wagner Maciel', 1000 * 100)
ON CONFLICT DO NOTHING;
INSERT INTO customers (name, account_limit)
VALUES ('Walter White', 800 * 100)
ON CONFLICT DO NOTHING;
INSERT INTO customers (name, account_limit)
VALUES ('Wallace Brown', 10000 * 100)
ON CONFLICT DO NOTHING;
INSERT INTO customers (name, account_limit)
VALUES ('Wade Black', 100000 * 100)
ON CONFLICT DO NOTHING;
INSERT INTO customers (name, account_limit)
VALUES ('Warren Grey', 5000 * 100)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS transactions
(
    id          INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    value       INTEGER     NOT NULL,
    type        VARCHAR(1)  NOT NULL,
    description VARCHAR(10) NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_id INTEGER     NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

CREATE INDEX IF NOT EXISTS customers_transactions_idx ON transactions USING HASH (customer_id);

CREATE OR REPLACE FUNCTION credit_operation(
    request_customer_id INTEGER,
    request_value INTEGER,
    request_description VARCHAR(10))
    RETURNS TABLE
            (
                success       BOOLEAN,
                current_limit INTEGER,
                new_balance   INTEGER
            )
AS
$$
BEGIN
    PERFORM pg_advisory_xact_lock(request_customer_id);

    INSERT INTO transactions (value, type, description, customer_id)
    VALUES (request_value, 'c', request_description, request_customer_id);

    RETURN QUERY
        UPDATE customers
            SET balance = balance + request_value
            WHERE id = request_customer_id
            RETURNING TRUE, account_limit, balance;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION debit_operation(
    request_customer_id INTEGER,
    request_value INTEGER,
    request_description VARCHAR(10))
    RETURNS TABLE
            (
                success       BOOLEAN,
                current_limit INTEGER,
                new_balance   INTEGER
            )
AS
$$
DECLARE
    current_balance INTEGER;
    current_limit   INTEGER;
BEGIN
    PERFORM pg_advisory_xact_lock(request_customer_id);

    SELECT balance, account_limit INTO current_balance, current_limit FROM customers WHERE id = request_customer_id;

    IF current_balance - request_value >= current_limit * -1 THEN
        INSERT INTO transactions (value, type, description, customer_id)
        VALUES (request_value, 'd', request_description, request_customer_id);
        RETURN QUERY
            UPDATE customers
                SET balance = balance - request_value
                WHERE id = request_customer_id
                RETURNING TRUE, account_limit, balance;
    ELSE
        RETURN QUERY SELECT FALSE, current_limit, current_balance;
    END IF;
END;
$$ LANGUAGE plpgsql;
