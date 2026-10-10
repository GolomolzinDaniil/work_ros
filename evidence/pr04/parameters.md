## Обычный запуск при `hz = 10 Гц`
```bash
danya@danya-BRN-GXXXA:~/work_ros$ ros2 topic hz /turtle1/cmd_vel
average rate: 10.005
        min: 0.099s max: 0.101s std dev: 0.00046s window: 9
average rate: 10.001
        min: 0.099s max: 0.101s std dev: 0.00047s window: 19
average rate: 9.999
        min: 0.099s max: 0.101s std dev: 0.00042s window: 29
```

## Попытка установить `hz = 0 Гц`
Вывод ошибки
```bash
danya@danya-BRN-GXXXA:~/work_ros$ ros2 param set /patrol publish_hz 0.0
Setting parameter failed: Invalid 'publish_rate': 0.0. Must be [1., 30.]
```
Предыдущая частота не изменилась
```bash
danya@danya-BRN-GXXXA:~/work_ros$ ros2 topic hz /turtle1/cmd_vel
average rate: 9.995
        min: 0.099s max: 0.101s std dev: 0.00053s window: 9
average rate: 10.000
        min: 0.099s max: 0.101s std dev: 0.00047s window: 19
average rate: 10.000
        min: 0.099s max: 0.101s std dev: 0.00040s window: 29
```

## Установка валидных значений `hz = 5 Гц`
Установка удалась
```bash
danya@danya-BRN-GXXXA:~/work_ros$ ros2 param set /patrol publish_hz 5.873
Set parameter successful
```
Проверка установки
```bash
danya@danya-BRN-GXXXA:~/work_ros$ ros2 topic hz /turtle1/cmd_vel
average rate: 5.875
        min: 0.170s max: 0.171s std dev: 0.00040s window: 5
average rate: 5.874
        min: 0.169s max: 0.171s std dev: 0.00043s window: 11
average rate: 5.874
        min: 0.169s max: 0.171s std dev: 0.00039s window: 17
```

## Установка других значений

`ros2 param set /patrol linear_speed N` - установка новой линейной скорости

`ros2 param set /patrol turn_rate M` - условнока новой угловой скорости

`ros2 topic echo /turtle1/pose` - вывод текущей позы


## Работа с action и service

### Отправка цели
Действие поворта на заданный theta (в радианах):
```bash
ros2 action send_goal /turtle1/rotate_absolute turtlesim_msgs/action/RotateAbsolute '{theta: 1.57}' --feedback
```
P.S: повторный вызов на тот же аргумент не будет двигать черепаху

Сервис для отчистки пути черепахи
```bash
ros2 service call /clear std_srvs/srv/Empty '{}'
```