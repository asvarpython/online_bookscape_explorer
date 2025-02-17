-- 7. Find the Average Page Count for eBooks vs Physical Books

SELECT 
    CASE 
        WHEN isEbook = 1 THEN 'Ebook' 
        ELSE 'Physical Book' 
    END AS book_type, 
    AVG(pageCount) AS avg_page_count
FROM book_search
WHERE pageCount IS NOT NULL
GROUP BY isEbook;