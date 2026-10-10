"""Интеграционные тесты для ПР04: параметры и живой обмен ROS."""
import time

import pytest
import rclpy
from geometry_msgs.msg import Twist
from rcl_interfaces.msg import Parameter
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from turtlesim_msgs.msg import Pose

from patrol.patrol import Patrol


@pytest.fixture(scope='function')
def ros_context():
    """Изолированный контекст ROS для каждого теста."""
    rclpy.init(args=['--ros-args', '-r', '__ns:=/pr04_test'])
    yield
    rclpy.try_shutdown()


def _wait_for_condition(executor, condition, timeout=5.0):
    """Вспомогательная функция ожидания события в цикле событий."""
    deadline = time.monotonic() + timeout
    while not condition() and time.monotonic() < deadline:
        executor.spin_once(timeout_sec=0.05)
    if not condition():
        raise TimeoutError("Условие не выполнено за отведенное время")


def test_default_parameters_flow(ros_context):
    """
    Проверяем дефолтные значения: linear_speed=0.5, turn_rate=0.3.
    До получения позы — нули. После — дефолты.
    """
    node = Patrol()
    observer = Node('observer')
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    executor.add_node(observer)
    
    messages = []
    sub = observer.create_subscription(Twist, '/pr04_test/cmd_vel', messages.append, 10)
    pub = observer.create_publisher(Pose, '/turtle1/pose', 10)

    try:
        # 1. Ждем первых сообщений (нулевые, так как latest_pose == None)
        _wait_for_condition(executor, lambda: len(messages) >= 2)
        assert all(m.linear.x == 0.0 and m.angular.z == 0.0 for m in messages[:2])

        # 2. Публикуем позу
        pub.publish(Pose(x=1.0, y=1.0))
        
        # 3. Ждем команду с ДЕФОЛТНЫМИ скоростями (0.5, 0.3)
        _wait_for_condition(executor, lambda: any(m.linear.x == 0.5 and m.angular.z == 0.3 for m in messages))
        
    finally:
        executor.shutdown()
        node.destroy_node()
        observer.destroy_node()


def test_invalid_frequency_rejected(ros_context):
    """
    Стадия "Сломать": пробуем поставить publish_hz = 0.0.
    Ожидаем отказ (successful=False) и сохранение работы старого таймера.
    """
    node = Patrol()
    observer = Node('observer')
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    executor.add_node(observer)
    
    messages = []
    sub = observer.create_subscription(Twist, '/pr04_test/cmd_vel', messages.append, 10)
    pub = observer.create_publisher(Pose, '/turtle1/pose', 10)

    try:
        # Инициализация потока
        pub.publish(Pose(x=1.0, y=1.0))
        _wait_for_condition(executor, lambda: len(messages) > 0)
        
        # Запоминаем текущее количество сообщений
        initial_count = len(messages)
        
        # Попытка установить bad freq через прямой вызов колбэка
        bad_param = Parameter(name='publish_hz', value=0.0)
        result = node.check_params([bad_param])
        
        # Проверяем, что параметр был ОТКЛОНЕН
        assert result.successful is False, "Нулевая частота должна быть отклонена"
        
        # КРИТИЧЕСКИ ВАЖНО: Вместо sleep используем спиннинг экзекьютора
        # Даем время пройти нескольким тикам (10Гц -> ~5 тиков за 0.5 сек)
        # Мы явно крутим executor, чтобы ROS успел вызвать tick()
        start_time = time.monotonic()
        while time.monotonic() - start_time < 0.5:
            executor.spin_once(timeout_sec=0.01)
            
        # Проверяем, что пришли новые сообщения (таймер жив)
        assert len(messages) > initial_count, "Нода должна продолжать работать после отказа в параметре"
        
    finally:
        executor.shutdown()
        node.destroy_node()
        observer.destroy_node()


def test_valid_frequency_restart_timer(ros_context):
    """
    Стадия "Доказать": меняем publish_hz с 10 на 5 Гц.
    Проверяем, что частота сообщений реально упала.
    """
    node = Patrol()
    observer = Node('observer')
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    executor.add_node(observer)
    
    messages = []
    sub = observer.create_subscription(Twist, '/pr04_test/cmd_vel', messages.append, 10)
    pub = observer.create_publisher(Pose, '/turtle1/pose', 10)

    try:
        # Инициализация
        pub.publish(Pose(x=1.0, y=1.0))
        _wait_for_condition(executor, lambda: len(messages) > 0)
        
        # Меряем базовую частоту (дефолт 10 Гц)
        # Используем спиннинг вместо сна
        count_before = len(messages)
        start_time = time.monotonic()
        duration_target = 1.0 # Секунд
        
        while time.monotonic() - start_time < duration_target:
            executor.spin_once(timeout_sec=0.01)
            
        elapsed = time.monotonic() - start_time
        rate_10hz = (len(messages) - count_before) / elapsed
        
        # Меняем частоту на 5 Гц
        good_param = Parameter(name='publish_hz', value=5.0)
        result = node.check_params([good_param])
        assert result.successful is True, "Валидная частота должна быть принята"
        
        # Ждем стабилизации нового таймера (короткий спин)
        for _ in range(10):
             executor.spin_once(timeout_sec=0.01)
        
        # Меряем новую частоту
        count_mid = len(messages)
        start_time = time.monotonic()
        
        while time.monotonic() - start_time < duration_target:
            executor.spin_once(timeout_sec=0.01)
            
        elapsed_new = time.monotonic() - start_time
        rate_5hz = (len(messages) - count_mid) / elapsed_new
        
        # Проверка: новая частота должна быть примерно вдвое меньше старой
        # Допускаем погрешность планировщика ОС
        print(f"Rate 10Hz measured: {rate_10hz:.2f}, Rate 5Hz measured: {rate_5hz:.2f}")
        
        assert rate_5hz < rate_10hz * 0.7, f"Частота не упала достаточно: {rate_10hz} -> {rate_5hz}"
        # Проверяем, что она близка к 5.0 (допустим отклонение +- 2 Гц из-за overhead тестов)
        assert abs(rate_5hz - 5.0) < 2.0, f"Новая частота {rate_5hz} далека от ожидаемых 5.0 Hz"
        
    finally:
        executor.shutdown()
        node.destroy_node()
        observer.destroy_node()