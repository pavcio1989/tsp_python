import pandas as pd

from data_loader import DataLoader
from config import Config


class CityGraph:
    def __init__(self, config: Config):
        data_loader = DataLoader(config)

        self.city_list = data_loader.get_city_list()
        self.city_latitudes, self.city_longitudes = data_loader.get_coord()
        self.distance_matrix = data_loader.get_distance_matrix()

    def create_city_graph_df(self):
        df = pd.DataFrame({
            'city': self.city_list,
            'latitude': self.city_latitudes,
            'longitude': self.city_longitudes}
        )

        return df

