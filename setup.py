import sys, os
try:
    from setuptools import setup
except:
    from distutils.core import setup

if sys.version_info < (2,6):
    raise NotImplementedError("Sorry, you need at least Python 2.6 or Python 3.x to use simpledict.")
    
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
        
setup(
    name='simpledict',
    version='0.2.5',
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
    long_description=read('Readme.md'),
    test_suite="tests"
)

# python setup.py register sdist upload