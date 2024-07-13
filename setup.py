from setuptools import setup, find_packages

setup(
    name='bootloader_dump_tools',
    version='1.0.0',
    packages=find_packages(),
    url='',
    license='',
    author='',
    author_email='',
    description='',
    entry_points={
        "console_scripts": [
            "brntool=brntool:main",
            "cfenand=cfenand:main",
            "cfenandxyz=cfenandxyz:main",
            "cfetool=cfettool:main",
            "en751221tool=en751221tool:main",
            "rt63365tool=rt63365tool:main",
            "rtl867xtool=rtl867xtool:main",
            "trl8186tool=trl8186tool:main",
            "zyx1tool=zyx1tool:main",
            "zyx2tool=zyx2tool:main",
        ]
    }
)
