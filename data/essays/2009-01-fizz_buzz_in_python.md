# Fizz Buzz in Python
*January 2009*

Jeff Atwood of [Coding Horror](http://codinghorror.com) has developed a sure fire test to filter out *good programmers* from *bad ones*. It's called [the FizzBuzz test](http://www.codinghorror.com/blog/archives/000781.html), and it's a very simple problem to solve<label for="sn-fizzbuzz-test" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-fizzbuzz-test" class="margin-toggle"/><span class="sidenote">FizzBuzz became legendary in programming interviews because it revealed a shocking truth: many candidates who claimed programming experience couldn't write even the simplest code. The test exposes basic gaps in understanding loops, conditionals, and modular arithmetic.</span>.

```python
for i in range(1, 101):
    if not i % 15:
        print "FizzBuzz"
    elif not i % 3:
        print "Fizz"
    elif not i % 5:
        print "Buzz"
    else:
        print i
```