def minus(numbers):
    """
    Subtract a list of numbers.
    >>> minus([3, 1])
    2
    >>> minus([3, 2, 4])
    -3
    """
    return reduce(lambda x, y: x - y, numbers)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
