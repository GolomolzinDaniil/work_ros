import math
import pytest

from patrol.validate_params import valid_linear_speed, valid_turn_rate, valid_publish_hz
from patrol.control import choose_command

def test_linear_speed():
    '''
    Базовые тесты линейной скорости
    '''
    assert valid_linear_speed(float('inf')) is False
    assert valid_linear_speed(float('nan')) is False
    assert valid_linear_speed(-1.) is False
    assert valid_linear_speed(.5) is True
    assert valid_linear_speed(2.) is False

def test_turn_rate():
    '''
    Базовые тесты угловой скорости
    '''
    assert valid_turn_rate(float('inf')) is False
    assert valid_turn_rate(float('nan')) is False
    assert valid_turn_rate(-2.) is False
    assert valid_turn_rate(0.) is True
    assert valid_turn_rate(2.) is False

def test_publish_hz():
    '''
    Базовые тесты частоты публикации
    '''
    assert valid_publish_hz(float('inf')) is False
    assert valid_publish_hz(float('nan')) is False
    assert valid_publish_hz(0.) is False
    assert valid_publish_hz(15.) is True
    assert valid_publish_hz(31.) is False

def test_choose_command():
    '''
    Базовые тесты выбора аргументов для Twist
    '''
    fst, snd = choose_command(None, 0., 0.)
    assert fst == 0.
    assert snd ==0.

    fst, snd = choose_command(True, 1., 2.)
    assert fst == 1.
    assert snd == 2.