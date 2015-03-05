from setuptools import setup
try:
    import pypandoc
    description = pypandoc.convert('README.md','rst')
except:
    description=''

setup(
    name = "Sorty",
    version = '1.0.0',
    author = 'Pradipta Bora',
    author_email = 'pradd@outlook.com',
    description = "A File Sorting Magician for your PC built in Python",
    license = "MIT",
    keywords = "files sort utility",
    url = "https://github.com/geekpradd/Sorty",
    py_modules = ['sorty'],
    install_requires=[
          'argparse'   ],
    entry_points = {
    'console_scripts': ['sorty = sorty:main']
    },
    long_description=description,
    classifiers=[
     "Development Status :: 5 - Production/Stable",
          "Topic :: Utilities",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python"
    ],
)