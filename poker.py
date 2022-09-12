#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------


RANKS_VALUES = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}


def convert_rank_to_int(rank: str):
    """Конвертирует ранги из буквенных в числовые значения"""
    return int(rank) if rank.isdigit() else RANKS_VALUES[rank]


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)

    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    return sorted([_[0] for _ in hand], key=lambda rank: convert_rank_to_int(rank))


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    suits = set([card[-1] for card in hand])
    return True if len(suits) == 1 else False


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    straight_index = 1
    for index, item_value in enumerate(ranks):
        if index == 0:
            continue

        item_prev_value = ranks[index-1]
        item_prev = convert_rank_to_int(item_prev_value)
        item = convert_rank_to_int(item_value)

        if item - item_prev == 1:
            straight_index += 1
        else:
            straight_index = 0

        if straight_index == 5:
            return True

    return False


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    for item in ranks:
        count = ranks.count(item)
        if count == n:
            return item

    return None


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    for item in ranks:
        if ranks.count(item) == 2:
            return [item, item]
    return None


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    return max(itertools.combinations(hand, 5), key=hand_rank)


def best_wild_hand(hand):
    """best_hand но с джокерами"""


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])

    # Возвращает ['7C', '7D', '7H', '7S', 'TC'] потому что его ранг (7, '7', 'T')
    # выше чем (7, '7', 'J') у ['7C', '7D', '7H', '7S', 'JD']
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            # == ['7C', '7D', '7H', '7S', 'JD']
            == ['7C', '7D', '7H', '7S', 'TC']
            )
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')
    print()


if __name__ == '__main__':
    test_best_hand()
    # test_best_wild_hand()
