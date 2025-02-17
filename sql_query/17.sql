-- 17. Authors Who Published in the Same Year Under Different Publishers

SELECT book_authors, year, COUNT(DISTINCT publisher) AS publisher_count
FROM book_search
WHERE publisher != 'Unknown'
GROUP BY book_authors, year
HAVING publisher_count > 1;