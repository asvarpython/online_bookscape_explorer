-- 15. Year with the Highest Average Book Price

SELECT year, AVG(amount_retailPrice) AS avg_price
FROM book_search
GROUP BY year
ORDER BY avg_price DESC
LIMIT 1;