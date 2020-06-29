#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
import unittest

setuptools.setup(name='easyipc',
    version='0.0.5',
    description='Easy-to-use Python library for inter-process communications.',
    author='Luis C. Garcia-Peraza Herrera',
    author_email='luiscarlos.gph@gmail.com',
    license='MIT License',
    url='https://github.com/luiscarlosgph/easyipc',
    packages=['easyipc'],
    package_dir={'easyipc' : 'src'}, 
    test_suite = 'tests',
    install_requires = ['numpy'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
         ],
)
