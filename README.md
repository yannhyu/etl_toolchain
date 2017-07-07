# etl_toolchain

report a Python3.6.1 bug:

  File "c:\users\nobody\appdata\local\continuum\anaconda3\Lib\traceback.py", line 405
    result.append(f'  [Previous line repeated {count-3} more times]\n')
                                                                     ^
SyntaxError: invalid syntax


+++++++++++++++++++++++++++++++++++++++++++++++++++++

result.append(f'  [Previous line repeated {count-3} more times]\n')
result.append('  [Previous line repeated {} more times]\n'.format(count-3))

report@bugs.python.org
