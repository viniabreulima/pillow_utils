from setuptools import setup, find_packages

setup(
    name='pillow-utils',
    version='0.0.01',
    description='Pillow snippets',
    author=['Vinicius Lima'],
    author_email='eu@viniciuslima.com',
    url='https://github.com/viniabreulima/pillow_utils',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    install_requires = [
        "pillow",
    ],
)
