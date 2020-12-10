from setuptools import setup
import os

setup(
    name="glitch_face",
    version="0.0.2",
    license="GPL",
    description="Face anon with pixelation and glitch",
    author="git314",
    author_email="git314@tutanota.com",
    url="https://github.com/git314/glitch_face",
    download_url="https://github.com/git314/glitch_face/releases/tag/0.0.1",
    keywords=["glitch", "facial", "detection", "face", "anonymity", "anonymous", "blur face", "pixelate face"],
    py_modules=["glitch_face"],
    install_requires=["Click", "opencv-python", "numpy"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
    ],
    entry_points="""
      [console_scripts]
      glitch_face=glitch_face:main
      """,
)
