-- Сервис формирования списка подарков: проверяемые запросы ПР7.

-- 1. SELECT: именованные списки подарков.
SELECT id, name
FROM gift_lists
ORDER BY id;

-- 2. SELECT: все подарки по возрастанию цены.
SELECT id, name, price, purchased, gift_list_id, occasion_id
FROM gifts
ORDER BY price, id;

-- 3. WHERE: подарки не дороже 3000 рублей.
SELECT id, name, price
FROM gifts
WHERE price <= 3000
ORDER BY price, name;

-- 4. WHERE: ещё не купленные подарки.
SELECT id, name, price
FROM gifts
WHERE purchased = 0
ORDER BY price DESC;

-- 5. WHERE: события не раньше 2026-11-01.
SELECT id, name, event_date, recipient_id
FROM occasions
WHERE event_date >= '2026-11-01'
ORDER BY event_date;

-- 6. JOIN: полная информация о подарках и связанных объектах.
SELECT
    gifts.id,
    gifts.name,
    gifts.price,
    gifts.purchased,
    occasions.name AS occasion_name,
    occasions.event_date,
    recipients.name AS recipient_name
FROM gifts
JOIN gift_lists ON gift_lists.id = gifts.gift_list_id
JOIN occasions ON occasions.id = gifts.occasion_id
JOIN recipients ON recipients.id = occasions.recipient_id
ORDER BY occasions.event_date, gifts.name;

-- 7. JOIN: события и их получатели.
SELECT
    occasions.id,
    occasions.name AS occasion_name,
    occasions.event_date,
    recipients.name AS recipient_name
FROM occasions
JOIN recipients ON recipients.id = occasions.recipient_id
ORDER BY occasions.event_date;

-- 8. Агрегат: количество подарков и полный бюджет.
SELECT COUNT(*) AS gifts_count, COALESCE(SUM(price), 0) AS total_price
FROM gifts;

-- 9. Агрегат: число и стоимость уже купленных подарков.
SELECT COUNT(*) AS purchased_count, COALESCE(SUM(price), 0) AS purchased_total
FROM gifts
WHERE purchased = 1;

-- 10. GROUP BY и JOIN: статистика по получателям.
SELECT
    recipients.id,
    recipients.name,
    COUNT(gifts.id) AS gifts_count,
    COALESCE(SUM(gifts.price), 0) AS total_price
FROM recipients
LEFT JOIN occasions ON occasions.recipient_id = recipients.id
LEFT JOIN gifts ON gifts.occasion_id = occasions.id
GROUP BY recipients.id, recipients.name
ORDER BY total_price DESC, recipients.name;

-- 11. GROUP BY и JOIN: статистика по событиям.
SELECT
    occasions.id,
    occasions.name,
    COUNT(gifts.id) AS gifts_count,
    COALESCE(SUM(gifts.price), 0) AS total_price
FROM occasions
LEFT JOIN gifts ON gifts.occasion_id = occasions.id
GROUP BY occasions.id, occasions.name
ORDER BY total_price DESC, occasions.name;

-- 12. GROUP BY: распределение подарков по статусу покупки.
SELECT purchased, COUNT(*) AS gifts_count, SUM(price) AS total_price
FROM gifts
GROUP BY purchased
ORDER BY purchased DESC;

-- 13. GROUP BY и HAVING: получатели как минимум с двумя подарками.
SELECT recipients.name, COUNT(gifts.id) AS gifts_count
FROM recipients
JOIN occasions ON occasions.recipient_id = recipients.id
JOIN gifts ON gifts.occasion_id = occasions.id
GROUP BY recipients.id, recipients.name
HAVING COUNT(gifts.id) >= 2
ORDER BY gifts_count DESC, recipients.name;

-- 14. WHERE с подзапросом: получатели без купленных подарков.
SELECT id, name
FROM recipients
WHERE id NOT IN (
    SELECT occasions.recipient_id
    FROM occasions
    JOIN gifts ON gifts.occasion_id = occasions.id
    WHERE gifts.purchased = 1
)
ORDER BY name;

-- 15. WHERE и JOIN: подарки выбранного получателя (пример id = 3).
SELECT gifts.id, gifts.name, gifts.price, occasions.name AS occasion_name
FROM gifts
JOIN occasions ON occasions.id = gifts.occasion_id
WHERE occasions.recipient_id = 3
ORDER BY occasions.event_date, gifts.name;
