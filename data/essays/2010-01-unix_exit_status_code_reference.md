# Unix Exit Status Code Reference

  I always find myself constantly Googling the list of unix status codes (typically defined in \`sysexits.h\`).{{< sidenote >}}These exit codes, standardized in BSD's sysexits.h, provide consistent return values for system programs. The tradition of using 0 for success and non-zero for various error conditions dates back to early Unix design principles.{{< /sidenote >}}

 
```
0 # successful termination64 # base value for error messages64 # command line usage error65 # data format error66 # cannot open input67 # addressee unknown68 # host name unknown69 # service unavailable70 # internal software error71 # system error (e.g., can't fork)72 # critical OS file missing73 # can't create (user) output file74 # input/output error75 # temp failure; user is invited to retry76 # remote error in protocol77 # permission denied78 # configuration error
```{{< sidenote >}}This quick reference helped countless developers avoid the tedium of looking up exit codes during system programming. The 64-78 range represents the standard BSD sysexits codes, with 64 (EX_USAGE) being particularly common in command-line tools.{{< /sidenote >}}
  