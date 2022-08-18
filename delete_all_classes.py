# ========== (c) JP Hwang 16/8/2022  ==========

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


def main():

    client = weaviate.Client("http://localhost:8080")
    client.schema.delete_all()  # deletes all classes along with the whole data

    return True


if __name__ == '__main__':
    main()
