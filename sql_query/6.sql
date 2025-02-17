-- 6. List Books with Discounts Greater than 20%

SELECT book_title, amount_listPrice, amount_retailPrice,
       ((amount_listPrice - amount_retailPrice) / amount_listPrice) * 100 AS discount_percentage
FROM book_search
WHERE amount_listPrice > 0 AND (amount_listPrice - amount_retailPrice) / amount_listPrice > 0.2;