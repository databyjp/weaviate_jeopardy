# ========== (c) JP Hwang 16/8/2022  ==========

import logging
import pandas as pd
import weaviate
import utils

# ===== SET UP LOGGER =====
logger = logging.getLogger(__name__)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh.setFormatter(formatter)
root_logger.addHandler(sh)
# ===== END LOGGER SETUP =====


from utils import client_uri
from utils import question_class


def load_data():
    df = pd.read_csv('data/JEOPARDY_CSV.csv')
    df.columns = [c.strip().lower() for c in df.columns]
    df['value'] = df['value'].str.replace("$", "").str.replace(",", "").str.replace('None', '0')
    df.rename({'question': 'clue'}, axis=1, inplace=True)
    return df


def check_batch_result(results: dict):
    """
    Check batch results for errors.

    Parameters
    ----------
    results : dict
        The Weaviate batch creation return value, i.e. returned value of the client.batch.create_objects().
    """

    if results is not None:
        for result in results:
            if 'result' in result and 'errors' in result['result']:
                if 'error' in result['result']['errors']:
                    print(result['result']['errors']['error'])
    return None


def import_data(client, df, cols, limit=100, use_batch=True):
    """
    Import data using batches
    :param client:
    :param df:
    :param cols: Column mapping between input DataFrame & DB
    :param limit: N rows
    :param use_batch: Boolean - use batches or not
    :return:
    """
    if len(df) < limit or limit is None:
        limit = len(df)
    print(f'Importing {limit} entries... please wait.')

    from datetime import datetime
    start_time = datetime.now()

    if use_batch:
        client.batch.configure(
            # `batch_size` takes an `int` value to enable auto-batching
            # (`None` is used for manual batching)
            batch_size=100,
            # dynamically update the `batch_size` based on import speed
            dynamic=False,
            # `timeout_retries` takes an `int` value to retry on time outs
            timeout_retries=3,
            # checks for batch-item creation errors
            callback=check_batch_result,
        )

    for i in range(limit):
        object_props = {c: df.iloc[i][c] for c in cols}
        if use_batch:
            with client.batch as batch:
                batch.add_data_object(object_props, question_class)
                # # When setting a custom vector
                # batch.add_data_object(object_props, "Question", vector=YOUR_VECTOR_HERE)
        else:
            client.data_object.create(
                object_props,
                question_class,
                # vector=YOUR_VECTOR_HERE  # When setting a custom vector
            )

    finish_time = datetime.now()
    elapsed_time = finish_time - start_time
    print(elapsed_time)
    return True


def main():

    client = weaviate.Client(client_uri)
    df = load_data()

    print(f'DB size before import: {utils.get_db_size()}')

    cols = ["category", "clue", "answer", "round", "value"]

    limit = len(df)
    limit = 10000  # Only import some for speed

    import_data(client, df, cols, limit, use_batch=True)

    print(f'DB size after import: {utils.get_db_size()}')

    return True


if __name__ == '__main__':
    main()
