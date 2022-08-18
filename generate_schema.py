# ========== (c) JP Hwang 5/8/2022  ==========

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

# Dataset to use:
# https://www.kaggle.com/datasets/tunguz/200000-jeopardy-questions

def main():

    import weaviate

    client = weaviate.Client("http://localhost:8080")

    schema = {
        "classes": [{
            "class": "Question",
            "description": "A Jeopardy! question with an answer",
            "properties": [
                {
                    "dataType": ["string"],
                    "description": "Category or topic of the question",
                    "name": "category"
                },
                {
                    "dataType": ["string"],
                    "description": "Round that the question was in",
                    "name": "round"
                },
                {
                    "dataType": ["string"],
                    "description": "Points value of the question.",
                    "name": "value"
                },
                {
                    "dataType": ["string"],
                    "description": "Clue provided to the contestants",
                    "name": "question"
                },
                {
                    "dataType": ["string"],
                    "description": "The correct answer",
                    "name": "answer"
                },
            ],
        }]
    }

    client.schema.create(schema)

    return True


if __name__ == '__main__':
    main()
