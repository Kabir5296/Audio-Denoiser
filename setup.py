from setuptools import setup, find_packages
import os
from pathlib import Path

ABSOLUTE_DIR = Path(__file__).parent

NAME = 'cleanunet-denoiser'
VERSION = '0.0.1' 
DESCRIPTION = 'CleanUNet based audio denoiser'
AUTHOR_WEBSITE = 'https://www.mahfuzulkabir.com/'
GITHUB_URL = 'https://github.com/Kabir5296/Audio-Denoiser.git'

AUTHOR = "A F M Mahfuzul Kabir"
AUTHOR_EMAIL = "<afmmahfuzulkabir@gmail.com>"

REQUIREMENTS = [
        'torchaudio==2.4.1',
        'numpy==2.0.2',
        'pandas==2.2.3',
        'soundfile==0.12.1',
        'scipy==1.13.1',
        'transformers==4.44.2',
        'cleanunet==0.0.3'
]
README = open('README.md').read()
PACKAGE_DATA = 'requirements.txt'

setup(
        name = NAME, 
        version = VERSION,
        
        description = DESCRIPTION,
        long_description = README,
        long_description_content_type = 'text/markdown',
        
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        
        license='MIT',
        packages = find_packages(where = 'denoiser'),
        include_package_data=True,
        package_data={'':['requirements.txt']},
        install_requires = REQUIREMENTS,
        
        classifiers = [
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9"
        ],
        
        keywords = ['audio denoise','denoise','cleanunet','speech denoise'],
        
        url = GITHUB_URL
)