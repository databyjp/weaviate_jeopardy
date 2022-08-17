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


def main():
    df = pd.read_csv("data/rotten_tomatoes_critic_reviews.csv")

    return True


if __name__ == '__main__':
    main()
