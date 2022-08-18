# ========== (c) JP Hwang 16/8/2022  ==========

import logging
import pandas as pd
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


def load_data():
    df = pd.read_csv('data/JEOPARDY_CSV.csv')
    df.columns = [c.strip().lower() for c in df.columns]
    df['value'] = df['value'].str.replace("$", "").str.replace(",", "").str.replace('None', '0')
    return df


def import_simple(client, df, cols, limit=100):

    if len(df) < limit or limit == None:
        limit = len(df)

    from datetime import datetime
    start_time = datetime.now()

    for i in range(limit):
        object_props = {c: df.iloc[i][c] for c in cols}

        client.data_object.create(
            object_props,
            "Question",
        )

    finish_time = datetime.now()
    elapsed_time = finish_time - start_time
    print(elapsed_time)
    return True


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


def import_batch(client, df, cols, limit=100):

    if len(df) < limit or limit == None:
        limit = len(df)

    from datetime import datetime
    start_time = datetime.now()

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
        with client.batch as batch:
            batch.add_data_object(object_props, 'Question')

    finish_time = datetime.now()
    elapsed_time = finish_time - start_time
    print(elapsed_time)
    return True


def main():
    client = weaviate.Client("http://localhost:8080")

    df = load_data()
    cols = ["category", "round", "value", "question", "answer"]

    import_batch(client, df, cols, 10000)

    return True


if __name__ == '__main__':
    main()
