## Перевод .xacro в .urdf
```bash
danya@danya-BRN-GXXXA:~/work_ros$ xacro src/course_description/urdf/vehicle.urdf.xacro > src/course_description/urdf/vehicle.urdf
```

## Проверка правильности .urdf
```bash
danya@danya-BRN-GXXXA:~/work_ros$ check_urdf src/course_description/urdf/vehicle.urdf
robot name is: my_robot
---------- Successfully Parsed XML ---------------
root Link: base_link has 6 child(ren)
    child(1):  front_left_wheel
    child(2):  front_right_wheel
    child(3):  imu_link
    child(4):  lidar_link
    child(5):  rear_left_wheel
    child(6):  rear_right_wheel
```