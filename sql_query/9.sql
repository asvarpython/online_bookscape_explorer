-- 9. List Publishers with More than 10 Books

SELECT publisher, COUNT(*) AS book_count
FROM book_search
WHERE publisher != 'Unknown'
GROUP BY publisher
HAVING book_count > 10;