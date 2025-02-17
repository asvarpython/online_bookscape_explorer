-- 5. Find Books Published After 2010 with at Least 500 Pages

SELECT book_title, year, pageCount
FROM book_search
WHERE year > 2010.0 AND year != 0 AND pageCount >= 500;