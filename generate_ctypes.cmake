# CMake function to generate Python ctypes bindings from C headers (using ctypeslib2)
# Requires ${PYTHON_COMMAND} to be set to an appropriate invocation of the python interpreter.
# E.g. if using CMake's FindPython, then ${Python_EXECUTABLE}, if using pipenv then "pipenv run python" or similar, etc.

# Generate Python bindings from C header(s) and corresponding shared library.
# Requires ctypeslib2, llvm clang
function(ctypesgen2_generate_python_bindings INPUT_LIBRARY_TARGET INPUT_LIBRARY_FILE OUTPUT_PY INPUT_HEADERS INPUT_FLAGS)
    add_custom_command(
        OUTPUT ${OUTPUT_PY}
        COMMAND ${PYTHON_COMMAND} ${CMAKE_CURRENT_SOURCE_DIR}/generate_ctypes.py
        --libclang-directory ${CLANG_SHARED_OBJECT_DIRECTORY}
        --libraries ${INPUT_LIBRARY_FILE}
        --flags="${FLAGS}"
        --headers ${INPUT_HEADERS}
        --output ${OUTPUT_PY}
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Generating Python ctypes bindings: ${OUTPUT_PY}"
        DEPENDS ${INPUT_HEADERS} ${INPUT_LIBRARY_TARGET} ${CMAKE_CURRENT_SOURCE_DIR}/generate_ctypes.py
        USES_TERMINAL
    )
    set_source_files_properties(${OUTPUT_PY} PROPERTIES GENERATED TRUE)
    
    # With no executable or library targets depending on the bindings, we use the ALL target
    add_custom_target(generate-${INPUT_LIBRARY_TARGET}-python ALL
        DEPENDS
            ${OUTPUT_PY}
            ${INPUT_LIBRARY_TARGET}
            ${CMAKE_CURRENT_SOURCE_DIR}/generate_ctypes.py
    )
endfunction()
