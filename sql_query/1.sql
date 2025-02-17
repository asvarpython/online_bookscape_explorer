-- 1. Check Availability of eBooks vs Physical Books

SELECT 
    CASE 
        WHEN isEbook = 1 THEN 'Ebook' 
        ELSE 'Physical Book' 
    END AS book_type, 
    COUNT(*) AS availability 
FROM book_search
GROUP BY isEbook
ORDER BY isEbook;