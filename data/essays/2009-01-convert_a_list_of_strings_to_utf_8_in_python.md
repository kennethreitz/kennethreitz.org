# Convert a List of Strings to UTF-8 in Python
*January 2009*





  If you'd like to learn more about programming, [contact me](/contact) for a one\-on\-one lesson.

```python
def utf8ify(list):
    '''Encode a list of strings in utf8'''
    return [item.encode('utf8') for item in list]
```

<label for="sn-python-utf8" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-python-utf8" class="margin-toggle"/><span class="sidenote">This 2009 code reflects Python 2's string handling challenges—the distinction between byte strings and Unicode strings that was eliminated in Python 3's unified string model. Modern Python developers rarely need such explicit encoding functions.</span>

  
