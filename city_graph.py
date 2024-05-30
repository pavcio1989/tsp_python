from data_loader import DataLoader


class CityGraph:
    def __init__(self, config):
        data_loader = DataLoader(config)

        self.city_list = data_loader.get_city_list()
        self.city_latitudes, self.city_longitudes = data_loader.get_coord()
        self.distance_matrix = data_loader.get_distance_matrix()

        self.best_tour = []
        self.best_distance = 0

    def reset_globals(self):
        self.best_tour = []
        self.best_distance = 1000000000

    # TODO: Add algorithms here
