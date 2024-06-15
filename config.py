import yaml


class Config:
    def __init__(self):
        with open('data.yml', 'r') as data_file:
            use_case = yaml.safe_load(data_file)

        self.use_case = use_case['data']['usecase']

        self.file_path = {}
        for filename in use_case['data']['filenames']:
            self.file_path[filename] = f"data/{self.use_case}/{use_case['data']['filenames'][filename]}"

        self.max_nodes = use_case['data']['max_nodes']

        with open('pipeline.yml') as pipeline_file:
            algo_list = yaml.safe_load(pipeline_file)

        self.algorithms = {}
        for algo_name in algo_list['algorithms']:
            self.algorithms[algo_name] = algo_list['algorithms'][algo_name]
