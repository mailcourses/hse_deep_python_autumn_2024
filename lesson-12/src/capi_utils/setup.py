from setuptools import setup, Extension


def run():
    setup(
        name="capi_fibs",
        version="1.0.0",
        ext_modules=[Extension("capi_fibs", ["capi_fibs.c"])],
    )



if __name__ == "__main__":
    run()
