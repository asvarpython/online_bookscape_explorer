-- 13. Books with the Same Author Published in the Same Year

SELECT book_authors, year, COUNT(*) AS book_count
FROM book_search
GROUP BY book_authors, year
HAVING book_count > 1;