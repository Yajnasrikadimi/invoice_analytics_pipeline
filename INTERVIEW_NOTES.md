# Interview notes: Invoice Analytics Pipeline

## 30-second pitch
"I built an invoice analytics pipeline on synthetic data. Python and Pandas clean and validate 5,000 invoices and track rejected rows. Clean data goes to S3, I load it into Redshift with COPY, calculate KPIs in SQL, and show them in a Power BI dashboard that drills from spend category down to individual invoices. I also added an Isolation Forest model that flags unusual invoices."

## Likely questions
- **Why S3 before Redshift?** S3 is cheap storage and the standard staging area. Redshift's COPY loads from S3 in parallel and is much faster than row-by-row inserts.
- **What did you clean?** Inconsistent status text, non-numeric amounts, invalid dates, duplicate invoice ids. Rejected rows are saved, not silently dropped.
- **How did you check correctness?** The same totals (4,888 rows, 12,419,740.57) in Pandas, SQLite and Redshift.
- **Why Isolation Forest?** No labels exist, so I needed an unsupervised method. I added features comparing each invoice with its customer and category average, and tested it by planting 10 inflated invoices (9 of 10 caught).
- **Limitations?** Synthetic data, Import-mode dashboard, manual AWS setup, no scheduler.
- **What would you do next?** Scheduling, tests, infrastructure as code, PySpark for scale.
- **Cost control?** Redshift Serverless at 4 RPU with a daily usage limit, AWS budget alert, and I deleted it after the project.
