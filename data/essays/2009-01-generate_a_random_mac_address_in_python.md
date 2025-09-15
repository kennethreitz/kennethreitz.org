# Generate a Random MAC Address in Python
*January 2009*

```python
import random

def randomMacAddress():
    """Returns a completely random Mac Address"""
    mac = [0x00, 0x16, 0x3e, 
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff), 
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

if __name__ == '__main__':
    print randomMacAddress()
```