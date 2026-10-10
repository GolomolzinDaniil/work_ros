def choose_command(pose, linear_speed: float, turn_rate: float):
    '''
    Выбор аргументов черепашки относительно ее позы
    '''
    if pose is None:
        return 0.0, 0.0
    return linear_speed, turn_rate
