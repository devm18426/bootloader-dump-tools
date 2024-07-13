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
            "brntool=bootloader_dump_tools.brntool:main",
            "cfenand=bootloader_dump_tools.cfenand:main",
            "cfenandxyz=bootloader_dump_tools.cfenandxyz:main",
            "cfetool=bootloader_dump_tools.cfetool:main",
            "en751221tool=bootloader_dump_tools.en751221tool:main",
            "rt63365tool=bootloader_dump_tools.rt63365tool:main",
            "rtl867xtool=bootloader_dump_tools.rtl867xtool:main",
            "trl8186tool=bootloader_dump_tools.trl8186tool:main",
            "zyx1tool=bootloader_dump_tools.zyx1tool:main",
            "zyx2tool=bootloader_dump_tools.zyx2tool:main",
        ]
    }
)
