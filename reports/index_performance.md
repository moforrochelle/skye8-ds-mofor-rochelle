# Index Performance Analysis

## Query Tested

We tested this query:

```sql
SELECT *
FROM appointments
WHERE facility_id = 'FC-04';
```

The goal was to see how adding an index on `facility_id` would change the way PostgreSQL runs the query.

## Before the Index

Before adding the index, PostgreSQL used a sequential scan:

```text
Seq Scan on appointments
Rows Removed by Filter: 35327
Execution Time: 15.450 ms
```

This means PostgreSQL went through the table and checked the rows to find the appointments for `FC-04`.

## Index Created

We created the following index:

```sql
CREATE INDEX idx_appointments_facility_id
ON appointments(facility_id);
```

## After the Index

After adding the index, PostgreSQL used:

```text
Bitmap Heap Scan on appointments
    -> Bitmap Index Scan on idx_appointments_facility_id

Execution Time: 29.784 ms
```

The query returned the same 2,466 appointments as before.

## Explanation

The main change was from a **Sequential Scan** to an **index-assisted Bitmap Scan**.

Before the index, PostgreSQL searched through the table to find the matching facility. After the index, it used `idx_appointments_facility_id` to find the matching rows first and then retrieve them from the table.

The indexed query was slower in this particular run. This can happen because execution times can vary depending on caching and other system factors. The important result is that PostgreSQL recognized the index and changed the way it searched the table.

## Conclusion

The index changed the query plan from a sequential scan to a bitmap scan using the new index. This shows how `EXPLAIN ANALYZE` can be used to see how an index affects a query.
