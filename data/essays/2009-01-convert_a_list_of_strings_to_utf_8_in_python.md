# Convert a List of Strings to UTF-8 in Python
*January 2009*

```python
def utf8ify(list):
    '''Encode a list of strings in utf8'''
    return [item.encode('utf8') for item in list]
```