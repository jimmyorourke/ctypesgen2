"""This script can be used to fully auto-generate Python bindings for C libraries, using libclang and ctypeslib.
This script wraps the ctypeslib codegenerator's generate_code function in much the same way as the clang2py tool
packaged with ctypeslib, however it provides more options and better handling for finding libclang, especially on
Windows, where when used in-build CMake doesn't seem to be able to properly set the PATH to the libclang location.
"""

import argparse
import os
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generate Python bindings from C header(s) and dynamic libraries")
    parser.add_argument("--libclang-directory", required=False, type=str, help="Directory containing libclang shared object (dylib / so / dll)")
    parser.add_argument("--headers", type=str, nargs="+", help="List of C Header(s) to export to Python")
    parser.add_argument("--libraries", type=str, nargs="+", help="Libraries to search for exported symbols")
    parser.add_argument("--flags", type=str, default="", help="Additional compiler flags to pass to clang")
    parser.add_argument("--output", type=str, help="Python wrapper file to generate")
    args = parser.parse_args()

    # Import Clang Wrapper
    # TODO: Is this still true?
    # On Windows, PATH is searched for libclang.dll, regardless of clang.cindex.Config, so prepend the Clang library directory to the path to ensure it is found.
    if os.name == "nt":
        os.environ['PATH'] = args.libclang_directory + os.pathsep + os.environ["PATH"]
    import clang.cindex
    clang.cindex.Config.set_library_path(args.libclang_directory)

    # Import ctypeslib2 Code Generator
    import ctypeslib
    from ctypeslib.codegen.codegenerator import generate_code
    from ctypeslib.codegen import typedesc

    from ctypes import CDLL, RTLD_LOCAL
    from ctypes.util import find_library

    # local library finding
    def load_library(name, mode=RTLD_LOCAL):
        ret = None
        if os.name == "nt":
            from ctypes import WinDLL
            # WinDLL does demangle the __stdcall names, so use that.
            ret = WinDLL(name, mode=mode)
        else:
            path = find_library(name)
            if path is None:
                # Maybe 'name' is not a library name in the linker style,
                # give CDLL a last chance to find the library.
                path = name
            ret = CDLL(path, mode=mode)
        if ret is None:
            raise Exception("Unable to open library %s" % name)
        return ret

    # Additional available types that we don't translate: Alias, Class, Macro.
    # We shouldn't have any aliases or classes in pure C code.
    # Enabling macros results in translation issues with the visibility attribute macros when being run as part of the build.
    types = (typedesc.Variable,
             typedesc.Structure,
             typedesc.Enumeration,
             typedesc.Function,
             typedesc.Structure,
             typedesc.Typedef,
             typedesc.Union)

    with open(args.output, 'w') as output:
        generate_code(srcfiles=args.headers, # files to generate python objects from
                      outfile=output,
                      expressions=None,
                      symbols=None,
                      verbose=True,
                      generate_comments=False, # get duplicated if a header is included multiple times
                      known_symbols=None,
                      searched_dlls=[load_library(d) for d in args.libraries],
                      types=types,
                      preloaded_dlls=None,
                      generate_docstrings=False, # neat but don't seem useful
                      generate_locations=False,
                      filter_location=True,
                      flags=args.flags.split(" ")
                      )
