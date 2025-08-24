# Generate a Random MAC Address in Python

  If you'd like to learn more about programming, [contact me](/contact-me/) for a one\-on\-one lesson.

  import random

  def randomMacAddress():"""Returns a completely random Mac Address"""mac \= \[0x00, 0x16, 0x3e, random.randint(0x00, 0x7f),random.randint(0x00, 0xff), random.randint(0x00, 0xff)]return ':'.join(map(lambda x: "%02x" % x, mac))

  if \_\_name\_\_ \=\= '\_\_main\_\_':print randomMacAddress()

  