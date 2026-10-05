# types.md — ПР02

## Топики

| Топик | Тип (Интерфейс) | Назначение |

/turtle1/cmd_vel - geometry_msgs/msg/Twist - Команда движения черепахи

/turtle1/pose - turtlesim_msgs/msg/Pose - Текущая поза черепахи

## Поля geometry_msgs/msg/Twist

```
danya@danya-BRN-GXXXA:~/work_ros$ ros2 interface show geometry_msgs/msg/Tw
ist
# This expresses velocity in free space broken into its linear and angular parts.

Vector3  linear
        float64 x
        float64 y
        float64 z
Vector3  angular
        float64 x
        float64 y
        float64 z
```