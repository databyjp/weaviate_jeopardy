# ========== (c) JP Hwang 16/8/2022  ==========

import logging
import pandas as pd
import numpy as np

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


def add_pub():
    import weaviate

    client = weaviate.Client("http://localhost:8080")
    example_data = {
        "name": "New York Times"
    }
    client.data_object.create(
        example_data,
        "Publication",
        "f81bfe5e-16ba-4615-a516-46c2ae2e5a80"
    )
    return True


def main():
    add_pub()
    import weaviate

    client = weaviate.Client("http://localhost:8080")

    example_data = {
        "name": "Stephen Holden"
    }

    client.data_object.create(
        example_data,
        "Critic",
        uuid="36ddd591-2dee-4e7e-a3cc-eb86d30a4301"
    )

    client.data_object.reference.add(
        "36ddd591-2dee-4e7e-a3cc-eb86d30a4301",
        "writesFor",
        "f81bfe5e-16ba-4615-a516-46c2ae2e5a80"
    )

    return True


if __name__ == '__main__':
    main()
