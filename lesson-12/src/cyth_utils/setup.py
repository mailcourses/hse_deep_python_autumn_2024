from setuptools import setup
from Cython.Build import cythonize


def main():
    setup(
        ext_modules=cythonize(["cyth_functions.pyx"])
    )


if __name__ == "__main__":
    main()
