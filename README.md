# Ecto-2

## Run the program
```
 $ ros2 launch ecto2 ecto2.launch.py
```

## Serial communication
Simple serial communication between arduino and the actuator. Will make it work with XRCE-DDS like [micro-ros](https://micro-ros.github.io/). But this should be suffic in the short term.

### Message
First byte defines command type. The next 4 bytes is an Int32 value for the command.

```
+-----------------+
|com\_type|value  |
+-----------------+
|1 byte   |4 byte |
+-----------------+
```

## Notes
### Pi camera permission problem
by default in ROS the account may not have correct access. Add user to `video` group would resolve this problem.
`$ sudo usermod -a -G video $USER`
