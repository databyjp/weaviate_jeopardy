# ========== (c) JP Hwang 16/8/2022  ==========

import logging
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

client_uri = utils.client_uri


def query_example(client):

    results = client.query.get(
        class_name='Question',
        properties="answer"
    ).with_limit(5).with_near_text({
        "concepts": ["Miley Cyrus"]
    }).do()
    print(results)

    return True


def get_question(client, category_query=None, n_questions=5):

    if category_query == None:
        category_query = 'pop music'

    results = client.query.get(
        class_name='Question',
        properties=["category", "question", "answer"]
    ).with_limit(n_questions).with_near_text({
        "concepts": [category_query]
    }).do()

    return results


def agg_example(client):

    result = client.query.aggregate("Question")\
        .with_group_by_filter(["category"]) \
        .with_fields('meta { count } category { topOccurrences { value } }') \
        .do()

    print(result)

    return True


def build_question(question):
    print(f"\nThe category is {question['category']}.")
    print(f"{question['question']}")
    input("Press any key when you want to see the answer...")
    print(f"{question['answer']}")
    return True


def main():
    client = weaviate.Client(client_uri)
    print(f"Getting results from our Jeopardy DB w/ {utils.get_db_size()} entries:")
    run_quiz = True
    while run_quiz:
        user_query = input("\nSuggest a topic! (like 'athletes', or 'pop stars'), press q to quit: ")
        if user_query == 'q':
            print('Byeeeeeee')
            break
        n_questions = 1
        results = get_question(client, category_query=user_query, n_questions=n_questions)
        if results is not None:
            for i in range(n_questions):
                # print(results['data']['Get']['Question'][i])
                build_question(results['data']['Get']['Question'][i])
        else:
            print("Hmm, something went wrong... sorry!")

    return True


if __name__ == '__main__':
    main()
