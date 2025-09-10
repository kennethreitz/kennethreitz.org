# Generate a Random MAC Address in Python
*January 2009*





> **Technical Context**: MAC (Media Access Control) addresses are unique identifiers for network interfaces. This code generates random MAC addresses, which was useful for network testing, virtualization, or privacy purposes in 2009. The specific vendor prefix used here (00:16:3e) belongs to Xensource, makers of the Xen hypervisor.

  If you'd like to learn more about programming, [contact me](/contact) for a one\-on\-one lesson.

  import random

> **Code Analysis**: This implementation uses a fixed vendor prefix (00:16:3e) while randomizing the last three octets. The constraint on the fourth octet (0x00-0x7f) ensures the locally administered bit isn't set inappropriately. The use of hexadecimal formatting (%02x) ensures proper zero-padding for single-digit hex values.

  def randomMacAddress():"""Returns a completely random Mac Address"""mac \= \[0x00, 0x16, 0x3e, random.randint(0x00, 0x7f),random.randint(0x00, 0xff), random.randint(0x00, 0xff)]return ':'.join(map(lambda x: "%02x" % x, mac))

  if \_\_name\_\_ \=\= '\_\_main\_\_':print randomMacAddress()

> **Python 2 Artifact**: This code is written in Python 2 (note the print statement without parentheses), reflecting the era when Python 2 was still dominant. In modern Python 3, this would require print() function syntax and potentially different string handling approaches.

  
