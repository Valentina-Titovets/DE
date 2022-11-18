--1 Вывести количество фильмоы в каждой категории, отсортировать по убыванию
SELECT cat."name" AS category_name, count(fil.film_id) AS count_film FROM film fil 
JOIN film_category fc 
ON fil.film_id = fc.film_id
JOIN category cat 
ON cat.category_id = fc.category_id
GROUP BY cat."name" 
ORDER BY count_film DESC ;




--2 Вывести 10 актеров, чьи фильмы больше всего арендовали, отсортировать по убыванию 
SELECT act.first_name ||' '|| act.last_name AS actor_name, count(ren.rental_id) AS count_rent 
FROM actor act 
JOIN film_actor fa 
ON act.actor_id =fa.actor_id 
JOIN film fil 
ON fil.film_id = fa.film_id 
JOIN inventory inv 
ON inv.film_id = fil.film_id 
JOIN rental ren 
ON ren.inventory_id = inv.inventory_id 
GROUP BY act.first_name, act.last_name 
ORDER BY count_rent DESC 
LIMIT 10;




--3 Вывести категорию фильмоы, на которую потратили больше всего денег
SELECT cat."name" AS category_name, sum(pa.amount)  AS sum_money
FROM payment pa 
INNER JOIN rental ren 
ON pa.rental_id = ren.rental_id 
INNER JOIN inventory inv 
ON inv.inventory_id = ren.inventory_id 
INNER JOIN film fil 
ON fil.film_id = inv.film_id 
INNER JOIN film_category fc 
ON fil.film_id = fc.film_id
INNER JOIN category cat 
ON cat.category_id = fc.category_id
GROUP BY cat."name" 
ORDER BY sum_money DESC 
LIMIT 1;




--4 Вывести названия фильмов, которых нет в инвентору. Написать запрос без использования IN.
SELECT fil.film_id, fil.title 
FROM film fil 
JOIN inventory inv 
ON inv.film_id = fil.film_id 
WHERE inv.inventory_id IS NULL ;






--5 Вывести топ 3 актеров, которые появлялись больше всего в категории "Сhildren"
SELECT ac.first_name ||' '|| ac.last_name AS actor_full_name, count(fil.film_id) AS cou_fil
FROM actor ac 
JOIN film_actor fa 
ON ac.actor_id =fa.actor_id 
JOIN film fil 
ON fil.film_id = fa.film_id 
WHERE fil.film_id IN 
(SELECT f.film_id FROM film f 
JOIN film_category fc 
ON f.film_id = fc.film_id
JOIN category ca 
ON ca.category_id = fc.category_id
WHERE ca."name" = 'Children')
GROUP BY ac.first_name,ac.last_name
HAVING count(fil.film_id) >3
ORDER BY cou_fil DESC ;





--6 Вывести города  с количеством активных и неактивных клиентов. Отсортировать по количеству неактивных клиентов по убыванию.
SELECT cit.city,
SUM(CASE WHEN cust.active = 1 THEN 1 ELSE 0 END) AS active,
SUM(CASE WHEN cust.active = 0 THEN 1 ELSE 0 END) AS no_active
FROM customer cust
INNER JOIN address add
ON add.address_id = cust.address_id
INNER JOIN city cit
ON cit.city_id = add.city_id
GROUP BY cit.city
ORDER BY SUM(CASE WHEN cust.active = 0 THEN 1 ELSE 0 END) DESC;


--7.Вывести категорию фильмов, у которой самое большое количество часов сумарной аренды в городах
SELECT * 
FROM 
       (SELECT category_id,
         category_name,
         city_a,
	 DENSE_RANK() OVER (ORDER BY city_a DESC) AS rank_city_a,
	 city_with_,
	 DENSE_RANK() OVER (ORDER BY city_with_ DESC) AS rank_city_
FROM (SELECT cat.category_id AS category_id,
       	cat.name AS category_name,
	SUM(CASE WHEN cit.city LIKE 'a%' THEN EXTRACT(DAY FROM ren.return_date - ren.rental_date) ELSE 0 END) as city_a,
	SUM(CASE WHEN cit.city LIKE '%-%' THEN EXTRACT(DAY FROM ren.return_date - ren.rental_date)  ELSE 0 END) as city_with_
	FROM rental ren
	INNER JOIN customer cus 
	ON ren.customer_id = cus.customer_id 
	INNER JOIN address ad
	ON cus.address_id = ad.address_id 
	INNER JOIN city cit
	ON cit.city_id = ad.city_id 
	INNER JOIN inventory inv 
	ON ren.inventory_id = inv.inventory_id 
	INNER JOIN film fil 
	ON inv.film_id = fil.film_id 
	INNER JOIN film_category fc 
	ON fil.film_id = fc.film_id 
	INNER JOIN category cat 
	ON cat.category_id = fc.category_id
	GROUP BY cat.category_id, cat.name) AS asb ) AS adf
WHERE rank_city_a = 1 OR rank_city_ = 1;