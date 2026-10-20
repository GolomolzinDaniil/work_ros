import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from turtlesim_msgs.msg import Pose

'''
class ReliabilityPolicy(QoSPolicyEnum):
    """
    Enum for QoS Reliability settings.

    This enum matches the one defined in rmw/types.h
    """

    # то, что ros2 установил по умолчанию (сам решит типо)
    SYSTEM_DEFAULT = 0
    
    # гарантия доставки сообщений. ВОзможны задержки
    RELIABLE = 1

    # отправка сообщений без гарантии доставки
    BEST_EFFORT = 2

    # служебка
    UNKNOWN = 3

    # адаптивная настройка политики. (выберет то, что нужно)
    BEST_AVAILABLE = 4
'''

    
class PoseRelay(Node):
    def __init__(self):

        super().__init__('pose_relay')
        
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            depth=10
        )
        
        self.publisher = self.create_publisher(
            Pose, 'sensor_pose', qos
        )
        self.subscription = self.create_subscription(
            Pose, 'pose', self.callback, 10
        )
    
    def callback(self, msg):
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = PoseRelay()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()