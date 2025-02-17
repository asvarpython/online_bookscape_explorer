-- 18. Average Retail Price of eBooks vs Physical Books

SELECT 
    AVG(CASE WHEN isEbook = 1 THEN amount_retailPrice END) AS avg_ebook_price,
    AVG(CASE WHEN isEbook = 0 THEN amount_retailPrice END) AS avg_physical_price
FROM book_search;