-- 12. Books with Ratings Count Greater Than the Average

SELECT book_title, ratingsCount
FROM book_search
WHERE ratingsCount > (SELECT AVG(ratingsCount) FROM book_search);