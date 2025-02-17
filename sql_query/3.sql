-- 3. Identify the Publisher with the Highest Average Rating

SELECT publisher, AVG(averageRating) AS avg_rating
FROM book_search
WHERE averageRating IS NOT NULL AND publisher != 'Unknown'
GROUP BY publisher
ORDER BY avg_rating DESC
LIMIT 1;