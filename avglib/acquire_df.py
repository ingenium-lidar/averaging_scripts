import pandas as pd
import json

def load_df(config_path = "averaging_config.json"):
    with open(config_path, "r") as f:
        config = json.load(f)

    df = pd.DataFrame(pd.read_csv(config["input_path"], sep=' ', header=None))

    df = df[list(range(3))]

    df.columns = ["x", "y", "z"]

    return df