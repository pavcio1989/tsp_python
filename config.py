import yaml


class Config:
    def __init__(self):
        with open('data.yml', 'r') as file:
            use_case = yaml.safe_load(file)

        self.use_case = use_case['data']['usecase']

        self.file_path = {}

        for filename in use_case['data']['filenames']:
            self.file_path[filename] = f"../data/{self.use_case}/{use_case['data']['filenames'][filename]}"
