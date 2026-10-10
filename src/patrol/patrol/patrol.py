import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node

from patrol.control import choose_command
from rcl_interfaces.msg import SetParametersResult

from turtlesim_msgs.msg import Pose

from patrol.validate_params import valid_linear_speed, valid_turn_rate, valid_publish_hz


class Patrol(Node):

    def __init__(self):

        super().__init__('patrol')

        self.declare_parameter('linear_speed', .5)
        self.declare_parameter('turn_rate', .3)
        self.declare_parameter('publish_hz', 10.)

        self.latest_pose = None
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.on_pose, 10
        )
        self.publisher = self.create_publisher(
            Twist, 'cmd_vel', 10
        )
        self.timer = self.create_timer(
            0.1, self.tick
        )
        # добавим чекер для параметров
        self.add_on_set_parameters_callback(self.check_params)


    def check_params(self, params):
        '''
        Чекер новых переданных параметров
        '''
        result = SetParametersResult(successful=True, reason='')

        for param in params:
            if param.name == 'linear_speed':
                new_linear_speed = param.value
                if not valid_linear_speed(new_linear_speed):
                    result.successful = False
                    result.reason = f"Invalid 'linear_speed': {new_linear_speed}. Must be [0., 1.]"
                    break
            elif param.name == 'turn_rate':
                new_turn_rate = param.value
                if not valid_turn_rate(new_turn_rate):
                    result.successful = False
                    result.reason = f"Invalid 'turn_rate': {new_turn_rate}. Must be [-1., 1.]"
                    break
            elif param.name == 'publish_hz':
                new_publish_rate = param.value
                if not valid_publish_hz(new_publish_rate):
                    result.successful = False
                    result.reason = f"Invalid 'publish_rate': {new_publish_rate}. Must be [1., 30.]"
                    break
                # частота изменилась, пересоздадим таймер
                self.remake_timer(new_publish_rate)
        return result


    def remake_timer(self, new_hz: float):
        '''
        Пересоздание таймера
        '''
        self.timer.cancel()
        self.timer = self.create_timer(1./new_hz, self.tick)
        

    def on_pose(self, message):
        '''
        Сеттер новой позы черепахи
        '''
        self.latest_pose = message

    def tick(self):
        '''
        Callback функция для таймера
        '''
        twist = Twist()
        twist.linear.x, twist.angular.z = choose_command(
            self.latest_pose,
            self.get_parameter('linear_speed').value,
            self.get_parameter('turn_rate').value
        )
        self.publisher.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = Patrol()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
