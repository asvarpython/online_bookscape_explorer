-- 20. Publisher with Highest Average Rating (Min 10 Books Published)

SELECT publisher, AVG(averageRating) AS avg_rating, COUNT(*) AS book_count
FROM book_search
WHERE averageRating IS NOT NULL AND publisher != 'Unknown'
GROUP BY publisher
HAVING book_count > 10
ORDER BY avg_rating DESC
LIMIT 1;