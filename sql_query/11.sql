-- 11. Retrieve Books with More than 3 Authors

SELECT book_title, book_authors
FROM book_search
WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) >= 3;