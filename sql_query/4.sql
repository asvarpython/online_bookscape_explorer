-- 4. Get the Top 5 Most Expensive Books by Retail Price

SELECT book_title, amount_retailPrice, currencyCode_retailPrice
FROM book_search
ORDER BY amount_retailPrice DESC
LIMIT 5;