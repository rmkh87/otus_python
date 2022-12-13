#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import update_wrapper, wraps, reduce


def disable(*args, **kwargs):
    """
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:
    """
    def inner(func):
        return func

    return inner


def decorator(func):
    """
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return update_wrapper(inner, func)


def countcalls(func):
    """Decorator that counts calls made to the function decorated."""
    @wraps(func)
    def inner(*args, **kwargs):
        inner.calls += 1
        return func(*args, **kwargs)

    inner.calls = 0
    return inner


def decorator_get_params(f):
    """
        Декоратор для передачи параметров с предыдущего декоратора.
        Чтобы декоратор, который выше (memo) не затирал аттрибуты
        декоратора, который ниже, напримере foo.
    """
    @wraps(f)
    def inner_first(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if hasattr(f, 'calls'):
                inner.calls = f.calls
            return result
        return inner

    return inner_first


def memo(func):
    """
    Memoize a function so that it caches all return values for
    faster future lookups.
    """

    @wraps(func)
    @decorator_get_params(func)
    def inner(*args, **kwargs):
        key = (func.__name__, tuple([_ for _ in args]), tuple(kwargs.items()),)
        if key not in inner.cache.keys():
            inner.cache[key] = func(*args, **kwargs)

        return inner.cache[key]

    inner.cache = dict()
    return inner


def n_ary(func):
    """
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    """
    @wraps(func)
    def inner(*args):
        def reducer(counter, item):
            return func(counter, item)

        return reduce(reducer, args[1:][::-1], args[0])

    return inner


def trace(indent):
    def inner_decorator(func):
        count = 0

        @wraps(func)
        def inner(number: int):
            nonlocal count
            space = ''.join([indent for _ in range(0, count)])

            count += 1
            print(f'{space}--> fib({number})')
            result = func(number)
            count -= 1
            print(f'{space}<-- fib({number}) == {result}')

            return result

        return inner

    return inner_decorator

# trace = disable


@memo
@countcalls
@n_ary
def foo(a, b):
    """Function foo"""
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    """Function bar"""
    return a * b


@countcalls
@trace("    ")
@memo
def fib(n):
    """Function fib"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo.__doc__)
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3, 2, 5))
    print(foo(4, 2, 0))
    print(foo(4))
    print("foo was called", foo.calls, "times")

    print()
    print(bar.__doc__)
    print(bar(4, 3))
    print(bar(5, 3, 2))
    print(bar(4, 3, 2, 1))
    print(bar(1, 2, 3, 2, 1))
    print("bar was called", bar.calls, "times")

    print()
    print(fib.__doc__)
    fib(3)
    print(fib.calls, 'calls made')


if __name__ == '__main__':
    main()
