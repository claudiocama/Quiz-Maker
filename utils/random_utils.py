import random


def select_random_objects(input_array, num_objects):
    num_objects = min(num_objects, len(input_array))
    random_objects = random.sample(input_array, num_objects)
    return random_objects

