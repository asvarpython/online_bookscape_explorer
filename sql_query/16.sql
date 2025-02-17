-- 16. Count Authors Who Published 3 Consecutive Years

SELECT book_authors, COUNT(DISTINCT year) AS year_count
FROM book_search
GROUP BY book_authors
HAVING year_count >= 3;