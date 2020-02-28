import os
from glob import glob
from setuptools import find_packages
from setuptools import setup

package_name='ecto2'

setup (
    name=package_name,
    maintainer='Shayne Wang',
    maintainer_email='shaynexwang@gmail.com',
    description='Ecto2 with ROS2',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        (os.path.join('share', package_name), ['package.xml']),
        # Include all launch files.
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
        # Include parameter configs.
        (os.path.join('share', package_name), glob('config/*.yaml')),
    ],
    license='MIT',
    install_requires=['setuptools'],
    entry_points={
            'console_scripts': [
                    'bt_controller = ecto2.bt_controller:main',
                    'actuator = ecto2.actuator:main',
            ],
    },
)
