# Unix Exit Status Code Reference
*January 2010*

I always find myself constantly Googling the list of unix status codes (typically defined in `sysexits.h`).

```bash
0   # successful termination
64  # base value for error messages
65  # command line usage error
66  # data format error
67  # cannot open input
68  # addressee unknown
69  # host name unknown
70  # service unavailable
71  # internal software error
72  # system error (e.g., can't fork)
73  # critical OS file missing
74  # can't create (user) output file
75  # input/output error
76  # temp failure; user is invited to retry
77  # remote error in protocol
78  # permission denied
79  # configuration error
```

This quick reference helps avoid the tedium of looking up exit codes during system programming.