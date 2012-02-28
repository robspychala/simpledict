import sys
from distutils.core import setup

if sys.version_info < (2,6):
    raise NotImplementedError("Sorry, you need at least Python 2.6 or Python 3.x to use bottle.")
    
setup(
    name='simpledict',
    version='0.1.1',
    description='Simple dictionary wrapper',
    author='Robert Spychala',
    author_email="robspychala@gmail.com",
    url="http://github.com/robspychala/simpledict",
    keywords=["dict", "mongo"],
    platforms=['any'],
    py_modules=['simpledict'],
    scripts=['simpledict.py'],
    license='MIT',
    classifiers=[
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            "Development Status :: 3 - Alpha",
            "Topic :: Database :: Database Engines/Servers",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
            ],
    long_description = """\
Makes dict modeling easy for document based databases with minimal extra funcitonality.

more info available at http://github.com/robspychala/simpledict

-----------------

  * Permissioning
  * Embedded documents
  * Minimization of field names
  * Python Properties
  * One python file
  * Doctests - functionality is unit tested

Missing features

  * No type system
  * No validation - up to you as the developer to add it.
"""
)