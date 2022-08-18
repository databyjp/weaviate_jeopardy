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


def query_example():

    client = weaviate.Client("http://localhost:8080")

    results = client.query.get(
        class_name='Question',
        properties="answer"
    ).with_limit(5).with_near_text({
        "concepts": ["Miley Cyrus"]
    }).do()
    print(results)

    return True


def get_question(category_query=None):

    if category_query == None:
        category_query = 'pop music'

    client = weaviate.Client("http://localhost:8080")

    results = client.query.get(
        class_name='Question',
        properties="category"
    ).with_limit(5).with_near_text({
        "concepts": [category_query]
    }).do()
    print(results)

    return results


def get_db_size():
    client = weaviate.Client("http://localhost:8080")
    result = client.query.aggregate("Question").with_fields('meta { count }').do()
    # print(result)
    return result['data']['Aggregate']['Question'][0]['meta']['count']


def agg_example():

    client = weaviate.Client("http://localhost:8080")

    result = client.query.aggregate("Question")\
        .with_group_by_filter(["category"]) \
        .with_fields('meta { count } category { topOccurrences { value } }') \
        .do()

    print(result)

    return True


def main():
    print(get_db_size())
    get_question(category_query='NFL football')
    get_question(category_query='Australian history')
    get_question(category_query='Cute Koalas')

    return True


if __name__ == '__main__':
    main()
