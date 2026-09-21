# Граф ROS 2: три состояния

## Исправный граф (домен 16)
- Ноды: /turtlesim, /teleop_turtle
- Топики: /turtle1/cmd_vel (teleop → turtlesim), /turtle1/pose (turtlesim → echo/hz)
- Частота /turtle1/pose: ~62 Гц (см. pose-hz.txt)
- Связь: полная, управление работает

## Разрыв связи (teleop в домене 17, turtlesim в 16)
- В домене 17: видна только /teleop_turtle, /turtlesim отсутствует (nodes-broken.txt)
- В домене 17: /turtle1/pose недоступен (pose-broken.txt пуст, exit=124 таймаут)
- В домене 16: /turtle1/pose читается, но поза не меняется после нажатия ↑ в B (pose-after-key-broken-control.txt == pose-before.txt)
- Причина: ROS_DOMAIN_ID изолирует DDS-домены; ноды в разных доменах не обнаруживают друг друга через discovery

## Восстановленный граф (оба в домене 16)
- Ноды: /turtlesim, /teleop_turtle (nodes-fixed.txt)
- /turtle1/pose доступен (pose-fixed.txt содержит данные, exit=0)
- После нажатия ↑ поза изменилась (pose-after-key-fixed.txt != pose-before.txt)
- Связь восстановлена полным возвратом teleop в домен 16
