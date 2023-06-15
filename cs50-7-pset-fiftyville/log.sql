-- Keep a log of any SQL queries you execute as you solve the mystery.
--take info on the crime commited
SELECT description FROM crime_scene_reports WHERE street = 'Humphrey Street' AND year = 2021 AND month = 7 AND day = 28;
--Result:Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
--Littering took place at 16:36. No known witnesses
--read interviews
SELECT transcript, id FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;
--ID 161 , 162, 163
--look for license plates that left the bakery within 10 minutes
 id  | year | month | day | hour | minute | activity | license_plate |
+-----+------+-------+-----+------+--------+----------+---------------+
| 260 | 2021 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
| 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 262 | 2021 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       |
| 263 | 2021 | 7     | 28  | 10   | 19     | exit     | 4328GD8       |
| 264 | 2021 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
| 265 | 2021 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
| 266 | 2021 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
| 267 | 2021 | 7     | 28  | 10   | 23     | exit     | 0NTHK55
--search fror transactions on atm
SELECT id,account_number,transaction_type,amount FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street';
id  | account_number | transaction_type | amount |
+-----+----------------+------------------+--------+
| 246 | 28500762       | withdraw         | 48     |
| 264 | 28296815       | withdraw         | 20     |
| 266 | 76054385       | withdraw         | 60     |
| 267 | 49610011       | withdraw         | 50     |
| 269 | 16153065       | withdraw         | 80     |
| 275 | 86363979       | deposit          | 10     |
| 288 | 25506511       | withdraw         | 20     |
| 313 | 81061156       | withdraw         | 30     |
| 336 | 26013199       | withdraw         | 35
--look for names of people who withdraw money from atm
SELECT * FROM people JOIN bank_accounts ON bank_accounts.person_id = people.id WHERE account_number =(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw');
id   |  name   |  phone_number  | passport_number | license_plate | account_number | person_id | creation_year |
+--------+---------+----------------+-----------------+---------------+----------------+-----------+---------------+
| 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       | 49610011       | 686048    | 2010          |
| 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       | 26013199       | 514354    | 2012          |
| 458378 | Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       | 16153065       | 458378    | 2012          |
| 395717 | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       | 28296815       | 395717    | 2014          |
| 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       | 25506511       | 396669    | 2014          |
| 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       | 28500762       | 467400    | 2014          |
| 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       | 76054385       | 449774    | 2015          |
| 438727 | Benista | (338) 555-6650 | 9586786673      | 8X428L0       | 81061156       | 438727    | 2018
--LICENSE PLATE and names of people who left the bakery in that time
  id   | name  |  phone_number  | passport_number | license_plate | account_number | person_id | creation_year |
+--------+-------+----------------+-----------------+---------------+----------------+-----------+---------------+
| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       | 49610011       | 686048    | 2010          |
| 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       | 26013199       | 514354    | 2012          |
| 396669 | Iman  | (829) 555-5269 | 7049073643      | L93JTIZ       | 25506511       | 396669    | 2014          |
| 467400 | Luca  | (389) 555-5198 | 8496433585      | 4328GD8       | 28500762       | 467400    | 2014
--search fro airport of the city
SELECT * FROM airports WHERE id = 4;
--Result: Csf Fiftyville Regional Airport
SELECT * FROM flights WHERE id = 36;
--Result:  36 | 4                      | 8    | 20     || 43 | 1                      | 9    | 30
--search for passenger of those 2 flights
SELECT * FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = 8 AND hour < 10) AND passport_number IN(SELECT passport_number FROM people JOIN bank_accounts ON bank_accounts.person_id = people.id WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'));
SELECT * FROM passengers WHERE passport_number = 5773159633;

SELECT * FROM phone_calls WHERE caller = '(367) 555-5533' AND year = 2021 AND month = 7 AND day = 28;

