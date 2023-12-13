-- 1. See theft description
SELECT *
FROM crime_scene_reports
WHERE day = 28 AND month = 7 and year = 2021 and street = 'Humphrey Street';

-- 2. See all interviews that mention bakery
SELECT *
FROM interviews
WHERE day = 28 AND month = 7 and year = 2021 and transcript LIKE "%bakery%" or "%Bakery%";

-- 3. See data from parking lot at the time of theft
SELECT *
FROM bakery_security_logs
WHERE day = 28 AND month = 7 AND year = 2021
AND hour = 10 AND minute BETWEEN 15 AND 25;

-- 4. Intersect of suspects that we know according to witnesses statements
SELECT name
FROM bakery_security_logs bss
JOIN people p ON bss.license_plate = p.license_plate
WHERE day = 28 AND month = 7 AND year = 2021
AND hour = 10 AND minute BETWEEN 15 AND 25
INTERSECT
SELECT name
FROM atm_transactions
JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number
JOIN people ON bank_accounts.person_id = people.id
WHERE day = 28 AND month = 7 AND year = 2021 AND transaction_type = 'withdraw'
AND atm_location = 'Leggett Street';

-- 5. See the earliest flight next day
SELECT *
FROM flights
WHERE year = 2021 AND day = 29 AND month = 7
ORDER BY hour LIMIT 1;

-- 6. See the name of the passangers that are in the list of suspects that we have from query 4 and we got the thief with this query
SELECT name
FROM flights f
JOIN passengers p ON f.id = p.flight_id
JOIN people pe ON p.passport_number = pe.passport_number
WHERE year = 2021 AND day = 29 AND month = 7 AND name IN ('Bruce', 'Diana', 'Iman', 'Luca')
ORDER BY hour LIMIT 1;

-- 7. See the city where he escape
SELECT city
FROM airports a
JOIN flights f ON f.destination_airport_id = a.id
WHERE f.id = 36;

-- 8. See the thief’s accomplice
SELECT name
FROM people p
JOIN phone_calls pc ON p.phone_number = pc.receiver
WHERE caller = (
    SELECT phone_number
    FROM people
    WHERE name = 'Bruce'
) AND year = 2021 AND month = 7 AND day = 28 AND duration < 60;

