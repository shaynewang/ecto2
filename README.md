# Ecto-2

## Run the program
```
 $ roslaunch ecto2 ecto2.launch
```

## Notes
### Pi camera permission problem
by default in ROS the account may not have correct access. Add user to `video` group would resolve this problem.
`$ sudo usermod -a -G video $USER`
