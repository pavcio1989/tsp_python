class CityGraph:
    def __init__(self, input):
        (
            self.city_list,
            self.city_latitudes,
            self.city_longitudes,
            self.distance_matrix
        ) = (
            self.get_city_data(input))

        # TODO: Make it global variables to be reset
        self.best_tour = []
        self.best_distance = 0

    def get_city_data(self, input):
        # TODO: Design data loading
        cities = []  # config.get("cities")
        lat = []  # config.get("latitudes")
        lon = []  # config.get("longitudes")
        dm = []  # config.get("distance_matrix")

        return cities, lat, lon, dm

    # TODO: Add algorithms here
