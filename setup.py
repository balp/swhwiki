import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    README = f.read()
with open(os.path.join(here, "CHANGES.txt")) as f:
    CHANGES = f.read()

requires = [
    'bcrypt',
    "deform",
    "plaster_pastedeploy",
    "pyramid",
    "pyramid_jinja2",
    "pyramid_tm",
    "sqlalchemy",
    "waitress",
    "zope.sqlalchemy",
]

dev_requires = [
    "pyramid_debugtoolbar",
]

tests_require = [
    "WebTest",
    "pytest",
    "pytest-cov",
]

setup(
    name="swhwiki",
    version="0.0",
    description="swhwiki",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="",
    author_email="",
    url="",
    keywords="web pyramid pylons",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        "testing": tests_require,
        "dev": dev_requires,
    },
    install_requires=requires,
    entry_points={
        "paste.app_factory": [
            "main = swhwiki:main",
        ],
        "console_scripts": ["initialize_tutorial_db = swhwiki.initialize_db:main"],
    },
)
