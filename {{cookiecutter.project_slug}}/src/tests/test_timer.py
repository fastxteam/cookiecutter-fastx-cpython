from src.decorators.timing import timer

@timer(unit='ms')
def heavy_task(n):
    total = sum(i ** 2 for i in range(n))
    return total

if __name__ == "__main__":
    heavy_task(100_000)
