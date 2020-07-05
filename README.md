# Ecto-2
It's nothing like the [Ecto-1](https://ghostbusters.fandom.com/wiki/Ecto-1) but one day it will drive itself.

Currently it's controlled by an Xbox One Controller. 

## Pairing Xbox One controller

Follow https://approxeng.github.io/approxeng.input/bluetooth.html

## Run the program
```
 $ ros2 launch ecto2 ecto2.launch.py
```

## Serial communication
Simple serial communication between arduino and the actuator. Will make it work with XRCE-DDS like [micro-ros](https://micro-ros.github.io/). But this should be suffic in the short term.

### Message
First byte defines the header. 

```
+----------------------------------+
|header |value1  |delimiter|value2 |
+----------------------------------+
|1 byte |2 bytes |1 byte   |2 bytes|
+----------------------------------+
```

Example message:
(-20,0) with 'H' as header and ':' as delimiter:

```
b'H\xff\xec:\x00\x00'
```

## Notes
### Pi camera permission problem
by default in ROS the account may not have correct access. Add user to `video` group would resolve this problem.
`$ sudo usermod -a -G video $USER`
