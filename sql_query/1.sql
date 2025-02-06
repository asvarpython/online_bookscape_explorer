#1 Check Availability of eBooks vs Physical Books
select  case when isebook = 0 then 'PhyscialBook' 
when isebook = 1 then 'Ebook' 
end as books, count(isebook) as availability 
from book_search
group by isebook
order by isebook ;