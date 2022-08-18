# ========== (c) JP Hwang 16/8/2022  ==========

import logging
import pandas as pd
import numpy as np
import weaviate

logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)

desired_width = 320
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', desired_width)


def load_data():
    df = pd.read_csv('data/JEOPARDY_CSV.csv')
    df.columns = [c.strip().lower() for c in df.columns]
    df['value'] = df['value'].str.replace("$", "").str.replace(",", "").str.replace('None', '0')
    return df


def main():
    client = weaviate.Client("http://localhost:8080")

    df = load_data()
    cols = ["category", "round", "value", "question", "answer"]

    from datetime import datetime
    start_time = datetime.now()

    for i in range(100):
        example_data = {c: df.iloc[i][c] for c in cols}

        client.data_object.create(
            example_data,
            "Question",
        )

    finish_time = datetime.now()
    elapsed_time = finish_time - start_time
    print(elapsed_time)

    return True


if __name__ == '__main__':
    main()
