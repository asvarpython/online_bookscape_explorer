-- 10. Find the Average Page Count for Each Category

SELECT categories, AVG(pageCount) AS avg_page_count
FROM book_search
WHERE pageCount IS NOT NULL
GROUP BY categories;