# ========== (c) JP Hwang 5/8/2022  ==========

import logging
import weaviate

# ===== SET UP LOGGER =====
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)
# ===== END LOGGER SETUP =====

# Dataset to use:
# https://www.kaggle.com/datasets/tunguz/200000-jeopardy-questions


def main():

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
