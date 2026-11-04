-- 1. Overall KPIs
SELECT COUNT(*)              AS total_invoices,
       SUM(amount)           AS total_amount,
       SUM(tax)              AS total_tax,
       SUM(amount + tax)     AS total_with_tax,
       AVG(amount)           AS average_invoice,
       MAX(amount)           AS largest_invoice
FROM invoices;

-- 2. Paid / Unpaid / Pending
SELECT status, COUNT(*) AS invoices, SUM(amount) AS total_amount
FROM invoices
GROUP BY status
ORDER BY total_amount DESC;

-- 3. Top 5 customers
SELECT customer, SUM(amount) AS total_amount
FROM invoices
GROUP BY customer
ORDER BY total_amount DESC
LIMIT 5;

-- 4. Spend by category
SELECT category, COUNT(*) AS invoices, SUM(amount) AS total_amount
FROM invoices
GROUP BY category
ORDER BY total_amount DESC;

-- 5. Monthly trend
SELECT DATE_TRUNC('month', invoice_date) AS month, SUM(amount) AS total_amount
FROM invoices
GROUP BY 1
ORDER BY 1;