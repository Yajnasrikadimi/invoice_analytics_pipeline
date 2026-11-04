-- Create the invoices table
CREATE TABLE invoices (
    invoice_id   VARCHAR(20),
    customer     VARCHAR(100),
    category     VARCHAR(50),
    amount       DECIMAL(12,2),
    tax          DECIMAL(12,2),
    invoice_date DATE,
    status       VARCHAR(20)
);

-- Load the cleaned data from S3
COPY invoices
FROM 's3://invoice-analytics-yajnasri-2026/clean/cleaned_invoices.csv'
IAM_ROLE default
FORMAT AS CSV
IGNOREHEADER 1;