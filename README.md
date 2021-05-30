# ctypesgen2

A wrapper tool around **@trolldbois**' [ctypeslib](https://github.com/trolldbois/ctypeslib) ([ctypeslib2](https://pypi.python.org/pypi/ctypeslib2/) on PyPi) for auto generating ctypes Python bindings of C source files, using libclang. 

This tool is comparable to the [clang2py](https://github.com/trolldbois/ctypeslib/blob/master/ctypeslib/clang2py.py) tool provided by ctypeslib2, but with a slightly different command line interface. In particular the libclang path is exposed as an argument. This is useful when generating python bindings as a build step of a C or C++ library, particularly on Windows where the PATH is searched for dlls like libclang. Build tools like CMake seem to have trouble modifying the PATH for some reason, unlike LD_LIBRARY_PATH on mac or linux which can be adjusted without issues.

Also provided
* A CMake script, defining a macro for invoking the tool, for generating ctypes bindings as part of the library build process.
* `ctypes_helpers`, some utilities for making ctypes easier to use. Includes a conversion from a `ctypes.Structure` to a python `dict`, and a means to replace `ctypes.Structure`'s `__str__` method with the stringification of such conversion.    

## Other ctypes generators
Reference of other generators I've come across.
I haven't had the chance to test these but the libclang ones are probably comparable. The non-libclang ones may not be cross-platform.
* Using libclang
  * [ctypes-binding-generator](https://github.com/clchiou/ctypes-binding-generator). Actually uses itself to generate the libclang bindings it uses!
  * **@osandov**'s [ctypesgen](https://github.com/osandov/ctypesgen). Looks quite simple but tests appear to show comprehensive functionality.
* Others
  * The original [ctypeslib](https://pypi.org/project/ctypeslib/). The codegen tool is based on gcc-xml.
  * **@davidjamesca**'s [ctypesgen](https://github.com/davidjamesca/ctypesgen). Invokes the C preprocessor, uses [Lex and Yacc](http://www.dabeaz.com/ply/).
  * [PyCParser](https://github.com/albertz/PyCParser). Actually a runtime C parser and interpreter with an automatic ctypes interface generator. 
  * [pyclibrary](https://github.com/MatthieuDartiailh/pyclibrary). Uses [pyparsing](https://github.com/pyparsing/pyparsing/) PEG parser. Fully encapsulates generated ctypes in an attempt to be a backend agnostic framework.
  * **@aristanetworks**' [ctypegen](https://github.com/aristanetworks/ctypegen). Requires C++ library building.
