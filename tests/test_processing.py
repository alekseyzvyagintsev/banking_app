#####################################################################
from typing import Any, Iterable

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize('value, state, expected', [
    (
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
        ],
        '',
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        ]
    )
])
def test_filter_by_state_state_executed(value: Iterable[dict[str, Any]],
                                        state: str, expected: list[dict[str, Any]]) -> None:
    assert filter_by_state(value, state) == expected


@pytest.mark.parametrize('value, state, expected', [
    (
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        ],
        'CANCELED',
        [
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        ]
    )
])
def test_filter_by_state_canceled(value: Iterable[dict[str, Any]], state: str, expected: list[dict[str, Any]]) -> None:
    assert filter_by_state(value, state) == expected


@pytest.mark.parametrize('value, state, expected', [
    (
        [
            {'id': 41428829, '_state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, '_state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, '_state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, '_state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
        ],
        '',
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        ]
    )
])
def test_filter_by_state_state_executed(value: Iterable[dict[str, Any]], state: str, expected: list[dict[str, Any]]) -> None:
    with pytest.raises(KeyError):
        assert filter_by_state(filter_by_state(value, state)) == expected


@pytest.mark.parametrize('value, descending, expected', [
    (
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
        ],
        '',
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        ]
    )
])
def test_sort_by_date_revers_true(value: Iterable[dict[str, Any]],  descending: bool, expected: list[dict[str, Any]]) -> None:
    assert sort_by_date(value, descending) == expected


@pytest.mark.parametrize('value, descending, expected', [
    (
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
        ],
        False,
        [
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        ]
    )
])
def test_sort_by_date_revers_false(value: Iterable[dict[str, Any]],  descending: bool, expected: list[dict[str, Any]]) -> None:
    assert sort_by_date(value, descending) == expected


@pytest.mark.parametrize('value, descending, expected', [
    (
        [
            {'id': 41428829, '_state': 'EXECUTED', '_date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, '_state': 'EXECUTED', '_date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, '_state': 'CANCELED', '_date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, '_state': 'CANCELED', '_date': '2018-10-14T08:21:33.419441'}
        ],
        '',
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        ]
    )
])
def test_sort_by_date_revers_true(value: Iterable[dict[str, Any]],  descending: bool, expected: list[dict[str, Any]]) -> None:
    with pytest.raises(KeyError):
        assert sort_by_date(value, descending) == expected

#####################################################################
