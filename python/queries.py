"""
query 1 Was Used For Initial Aggregation Of All Data Points. It Uses The sessions Table As The Base Table As
It Contains The Most Values
"""

"""
get_agg_users_query Aggregates All The Users Into One Via SQL. It Was Determined That Aggregations Should Be Done 
Using pandas Because It Would Either Be Very Very Slow To Process That One Using The Travel Tide Data Base Or Require 
The Viewer To Create Their Own Personal Database - Which I Initially Set It Up To Do - But That Would Create Too Many
Issues For A Person Just To View My Work Properly.
"""

query1 = """
    SELECT
        u.user_id,
        CASE WHEN gender = 'M' THEN 1 ELSE 0 END AS male,
        CASE WHEN gender = 'F' THEN 1 ELSE 0 END AS female,
        TRUNC(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - TO_TIMESTAMP(birthdate, 'YYYY-MM-DD')))/31557600) AS age,
        married::int,
        has_children::int,
        TRUNC(EXTRACT(EPOCH FROM ( CURRENT_TIMESTAMP - TO_TIMESTAMP(sign_up_date, 'YYYY-MM-DD')))) AS user_longevity_seconds,
        flight_booked::int,
        flight_discount_amount, 
        base_fare_usd,
        home_airport_lat, 
        home_airport_lon, 
        destination_airport_lat, 
        destination_airport_lon,
        EXTRACT(EPOCH FROM (TO_TIMESTAMP(session_end, 'YYYY-MM-DD HH24:MI:SS') - TO_TIMESTAMP(session_start, 'YYYY-MM-DD HH24:MI:SS'))) AS session_duration_seconds,
        page_clicks,
        hotel_booked::int,
        hotel_discount_amount,
        nights,
        rooms,
        TRUNC(EXTRACT(EPOCH FROM (TO_TIMESTAMP(check_out_time, 'YYYY-MM-DD') - TO_TIMESTAMP(check_in_time, 'YYYY-MM-DD')))) AS hotel_duration_seconds,
        hotel_per_room_usd,
        cancellation::int
    FROM sessions s
    LEFT JOIN flights f ON s.trip_id = f.trip_id
    LEFT JOIN users u ON u.user_id = s.user_id
    LEFT JOIN hotels h ON h.trip_id = s.trip_id
    GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
    ORDER BY user_id
"""


get_agg_users_query = """
    SELECT
        user_id,
        AVG(flight_booked) proportion_booked,
        AVG(flight_discount_amount) flight_average_discount,
        AVG(base_fare_usd) average_base_fare,
        TRUNC(AVG(age)) age,
        TRUNC(AVG(male)) male,
        TRUNC(AVG(female)) female,
        AVG(married) married,
        AVG(has_children) has_children,
        AVG(session_duration_seconds) average_session_time,
        AVG(user_longevity_seconds) user_longevity_seconds,
        AVG(page_clicks) average_clicks,
        AVG(cancellation) cancel_proportion,
        AVG(hotel_booked) hotel_booking_proportion,
        AVG(hotel_discount_amount) hotel_average_discount,
        AVG(nights) average_nights_booked,
        AVG(rooms) average_rooms_per_booking,
        AVG(hotel_duration_seconds) average_hotel_stay,
        AVG(hotel_per_room_usd) avg_price_per_room,
        AVG(distance) average_distance
FROM users_agg
GROUP BY user_id
ORDER BY user_id

"""