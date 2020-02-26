maintainer='Shayne Wang',
maintainer_email='shaynexwang@gmail.com',
description='Ecto2 with ROS2',
license='MIT',
entry_points={
        'console_scripts': [
                'bt_controller = ecto2.bt_controller:main',
                'actuator = ecto2.actuator:main',
        ],
},
