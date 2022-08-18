# ========== (c) JP Hwang 18/8/2022  ==========

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

client_uri = "http://localhost:8080"


def get_db_size():
    client = weaviate.Client(client_uri)
    result = client.query.aggregate("Question").with_fields('meta { count }').do()
    # print(result)
    return result['data']['Aggregate']['Question'][0]['meta']['count']


def main():
    return True


if __name__ == '__main__':
    main()
