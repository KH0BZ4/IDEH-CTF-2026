# Easy Rev Writeup

![Challenge](challenge.png)

**Category:** Reverse Engineering  
**Points:** 498  
**Solves:** 3  
**Author:** Bidr

## Challenge Description

> The beginning... and the end?

## Solution

This one was pretty simple. We get a binary called `chall`. When you run it, it just prints:

```
diagnose me please!!1!1!
```

Nothing useful there. So I opened it in a decompiler and looked at the main function:

```c
int32_t main(int32_t argc, char** argv, char** envp)
{
    void* const var_18 = "IDEH{beg1nn3r_rev_w3lcome}";
    puts("diagnose me please!!1!1!");
    return 0;
}
```

Lol the flag is just sitting there as a string but it's never printed. The hint "The beginning... and the end?" makes sense now - you need to look at the strings in the binary, not what it outputs.

You could also just run `strings` on it:

```bash
$ strings chall | grep IDEH
IDEH{beg1nn3r_rev_w3lcome}
```

## Flag

```
IDEH{beg1nn3r_rev_w3lcome}
```

Easy one to warm up!
