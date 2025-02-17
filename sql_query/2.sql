-- 2. Find the Publisher with the Most Books Published

SELECT publisher, COUNT(*) AS book_count
FROM book_search
WHERE publisher != 'Unknown'
GROUP BY publisher
ORDER BY book_count DESC
LIMIT 1;