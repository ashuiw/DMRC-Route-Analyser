def calculate_fare(number_of_stations):
    """
    TEMPORARY FARE ENGINE

    """
    if number_of_stations <= 3:
        return 10
    elif number_of_stations <= 8:
        return 20
    elif number_of_stations <= 15:
        return 30
    elif number_of_stations <= 25:
        return 40

    else:
        return 50