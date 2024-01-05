import numpy as np
from distance_formulas import *
from data_handlers import calc_time
import time
from math import ceil

""" 
A Collection Of Functions Used For Cleaning Data And Keeping The Jupyter Notebook Clean
"""



def add_metrics(DF):
    main_data = DF.copy()

    main_data["flight_ads"] = ((main_data["avg_flight_discount_amount"] * main_data["avg_base_fare_usd"])
                               / main_data["avg_distance"]
                               ).replace(np.nan, 0)

    main_data["hotel_ads"] = (main_data["avg_hotel_discount_amount"] * main_data["avg_hotel_per_room_usd"])
    # Below basically gives us a metric of time spent on average, not per day but per day per year * avg num clicks
    # This could give us skewed results as users may spend more or less time depending on how long they've been users
    # But I will scale the results to allow for some conformity
    main_data["dependents"] = main_data["prop_married"] + main_data["prop_has_children"]
    main_data["dependents"] = main_data["dependents"].astype("int64")
    main_data["sex"] = main_data["male"].apply(lambda y: 0 if y == 0.0 else 1)
    main_data["avg_hotel_stay_hours"] = main_data["avg_hotel_duration_seconds"] / 3600
    main_data["age"] = main_data["age"].astype("int64")
    return main_data


def metric_scaler(data_col):
    minimum = data_col.min()
    maximum = data_col.max()
    return (data_col - minimum) / (maximum - minimum)


def procure_main_data(main_data):
    main_data = add_metrics(main_data)
    main_data.drop(columns=[
        "avg_nights",
        "avg_base_fare_usd",
        "avg_hotel_per_room_usd",
        "avg_session_duration_seconds",
        "avg_user_longevity_seconds",
        "avg_page_clicks",
        "male",
        "female",
        "avg_distance",
        "prop_married",
        "prop_has_children",
        "avg_flight_discount_amount",
        "avg_hotel_discount_amount",
        "avg_hotel_duration_seconds",
        "prop_cancellation",
        "prop_hotel_booked",
    ], inplace=True)

    return main_data


def procure_all_data(DF):
    return add_metrics(DF)


def get_distance(DF, lat1: float, lon1: float, lat2: float, lon2: float, func: str = "haversine"):
    """
    :param DF:
    :param lat1:
    :param lon1:
    :param lat2:
    :param lon2:
    :param func: string ->
    "haversine" | anything else == "vincenty formula" :return: updated DataFrame with the entry locations removed and
    the final distance calculation in a new 'distance' column
    """
    start = time.time()
    if func == "haversine":
        distance_function = haversine
    else:
        distance_function = vincenty_distance

    DF['distance'] = DF.apply(
        lambda x: distance_function(
            x[lat1], x[lon1],
            x[lat2], x[lon2]
        ), axis=1)
    final = calc_time(start, time.time())
    print("Time To Finish Calculating Distances Was: ", final, "seconds.")
    return DF


def generate_bins(start_num: int | None, end_num: int | None = None, max_num: int | float | None = None,
    by: int | None = None, inclusive: bool = True, num_bins: int = None) -> tuple:


    if start_num is None and end_num is None:
        raise ValueError("The start_num and/or end_num must be provided.")
    if start_num is None or end_num is None:
        if start_num is None:
            start_num = 0
        if end_num is None:
            if max_num is not None:
                end_num = max_num
            else:
                end_num = start_num
                start_num = 0


    if max_num is None:
        max_num = end_num
    if num_bins is None:
        num_bins = max_num % start_num
    if by is None:
        by = (max_num // num_bins) - (max_num // num_bins) % 10

    if max_num > end_num:
        max_num = end_num

    bin_nums = [x for x in range(start_num, ceil(end_num), by)]

    bin_labels = []
    try:
        int(num_bins)
        bin_nums = bin_nums[0:num_bins+1]
    except ValueError:
        pass

    addendum = 1 if not inclusive else 0


    for index, bin_num in enumerate(bin_nums):
        start = bin_num
        if index != len(bin_nums) - 1:
            next_num = bin_nums[index + 1]
            end = next_num - addendum
            if index == len(bin_nums) - 2:
                if end > end_num:
                    bin_labels.append(f"{end}+")
                    return bin_nums, bin_labels
            bin_labels.append(f"{start}-{end}")
        else:
            bin_labels.append(f"{max_num}+")


    return bin_nums, bin_labels

