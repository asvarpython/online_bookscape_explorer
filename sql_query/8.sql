-- 8. Find the Top 3 Authors with the Most Books

SELECT book_authors, COUNT(*) AS book_count
FROM book_search
GROUP BY book_authors
ORDER BY book_count DESC
LIMIT 3;