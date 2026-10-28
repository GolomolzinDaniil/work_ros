# TF Tree Documentation

| Parent | Child | Joint Type | Expected Offset (xyz) | Publisher |
| :--- | :--- | :--- | :--- | :--- |
| base_link | lidar_link | fixed | [0.28, 0.0, 0.38] | robot_state_publisher |
| base_link | imu_link | fixed | [0.28, 0.0, 0.28] | robot_state_publisher |
| base_link | camera_link | fixed | [0.28, 0.0, 0.38] | robot_state_publisher |
| base_link | front_left_wheel | continuous | [0.4, 0.31, -0.1] | robot_state_publisher + joint_states |
| base_link | rear_left_wheel | continuous | [-0.4, 0.31, -0.1] | robot_state_publisher + joint_states |