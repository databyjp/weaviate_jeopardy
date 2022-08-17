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

def main():

    import weaviate

    client = weaviate.Client("http://localhost:8080")

    schema = {
        "classes": [{
            "class": "Publication",
            "description": "A publication with an online source",
            "properties": [
                {
                    "dataType": ["string"],
                    "description": "The title of the publication",
                    "name": "name"
                },
                {
                    "dataType": ["Review"],
                    "description": "The reviews this publication has",
                    "name": "hasArticles"
                },
            ],
        }, {
            "class": "Review",
            "description": "A movie review",
            "properties": [
                {
                    "dataType": ["string"],
                    "description": "The title of the review",
                    "name": "title"
                },
                {
                    "dataType": ["text"],
                    "description": "The body of the review",
                    "name": "body"
                },
            ],
        }, {
            "class": "Critic",
            "description": "The reviewer",
            "properties": [
                {
                    "dataType": ["string"],
                    "description": "Reviewer's name",
                    "name": "name"
                },
                {
                    "dataType": ["Review"],
                    "description": "Reviews the critic has written",
                    "name": "reviewsWritten"
                },
                {
                    "dataType": ["Publication"],
                    "description": "Publications the critic writes for",
                    "name": "writesFor"
                },
            ],
        }]
    }

    client.schema.create(schema)

    return True


if __name__ == '__main__':
    main()
