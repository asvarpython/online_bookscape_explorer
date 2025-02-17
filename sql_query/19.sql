-- 19. Identify Books with Ratings More Than Two Standard Deviations from the Average

SELECT book_title, FORMAT(averageRating, 1) AS averageRating, ratingsCount
FROM book_search
WHERE averageRating > (
        SELECT AVG(averageRating) + 2 * STDDEV(averageRating)
        FROM book_search
        WHERE averageRating IS NOT NULL
    )
   OR averageRating < (
        SELECT AVG(averageRating) - 2 * STDDEV(averageRating)
        FROM book_search
        WHERE averageRating IS NOT NULL
    );
