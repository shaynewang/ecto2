# Ecto-2

## Run the program
```
 $ ros2 launch ecto2 ecto2.launch.py
```

## Notes
### Pi camera permission problem
by default in ROS the account may not have correct access. Add user to `video` group would resolve this problem.
`$ sudo usermod -a -G video $USER`
