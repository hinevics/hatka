from dagster import job, op, get_dagster_logger
import random

@op
def get_random():
    r = [random.randint(0, 10) for _ in range(0, 100000)]
    return r[0]

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
