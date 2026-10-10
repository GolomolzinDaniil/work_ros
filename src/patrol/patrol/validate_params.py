import math


def valid_linear_speed(speed: float) -> bool:
    '''
    Валидация линейной скорости
    '''
    if not math.isfinite(speed):
        return False
    return 0. <= speed <= 1.

def valid_turn_rate(rate: float) -> bool:
    '''
    Валидация угловой скорости
    '''
    if not math.isfinite(rate):
        return False
    return -1. <= rate <= 1.

def valid_publish_hz(hz: float) -> bool:
    '''
    Валидация частоты публикации
    '''
    if not math.isfinite(hz):
        return False
    return 1. <= hz <= 30.
