import dvc.api


def load_data(init_dataset_path: str, loaded_dataset_path: str) -> None:
    with dvc.api.open(path=init_dataset_path) as fd:
        with open(loaded_dataset_path, "w") as f:
            f.write(fd.read())
