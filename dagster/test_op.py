from dagster import job, op, get_dagster_logger
import random

@op
def get_random():
    return random.randint(0, 10)

@op
def get_multi(rnd):
    return rnd*10

@op
def get_plus(rnd):
    return rnd+10

@op
def print_result(multi, plus):
    get_dagster_logger().info(f'Operation: {multi/plus}')


@job
def serial():
    rnd = get_random()
    multi = get_multi(rnd)
    plus = get_plus(rnd)
    print_result(multi, plus)
