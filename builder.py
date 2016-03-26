from hashlib import sha1
import random

# Global constants
BASE = 256
MAX = 2**BASE

random.seed(12345)

def createStaticIDs(size):
    """
    This creates |size| IDs
    The output will be the same each time we run this. 
    """
    
    population = sorted([int(sha1(bytes(str( random.random()), "UTF-8")).hexdigest(), 16) 
                         % MAX for x in range(size)])
    return population


def generateFileIDs(num):
    # Create num random file ids
    for _ in range(num):
        x = random.random()
        yield int(sha1(bytes(str(x), "UTF-8")).hexdigest(), 16) % MAX


