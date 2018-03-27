# Biscuit

A delicious tensor library.

## Stype Guide

### naming convention

for public class members: a underline with its name in small camel case.
for private class members: in small camel case.

```c++
class foo
{
private:
    int minBufferSize;
public:
    int _totalSize;
};
```

if the name is too long (over 4 words), use a namespace.

### pointers and reference

pointers and reference mark should next to variable rather than type.

```c++
int *data;
int &index;
int &ref(int i);
``` 

### namespace

namespaces should include a comment `//namespace xxx`.

```c++
namespace foo{
    /* code */
} // namespace foo
```

### preprocessor macros

except for some frequently used macros like `MIN`, `MAX`, etc, preprocessor macro should have an prefix which denotes the name of the project.

```c++
#define BS_MACRO_NAME
``` 

### comments

description should use doxygen styles.

```c++
/**
 * @brief this is a a brief description
 * /
```

other comments should have one space between `//` and your comments.

```c++
// comments
```
