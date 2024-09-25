from setuptools import setup, find_packages
import os

ABSOLUTE_DIR = os.path.abspath(os.path.dirname(__file__))

NAME = 'audio-denoiser'
VERSION = '0.0.1.dev1' 
DESCRIPTION = 'CleanUNet based audio denoiser'
AUTHOR_WEBSITE = 'https://www.mahfuzulkabir.com/'
GITHUB_URL = 'https://github.com/Kabir5296/Audio-Denoiser.git'

AUTHOR = "A F M Mahfuzul Kabir"
AUTHOR_EMAIL = "<afmmahfuzulkabir@gmail.com>"

REQUIREMENTS = open(os.path.join(ABSOLUTE_DIR,'requirements.txt')).read().splitlines()
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
        
        license = "MIT",
        packages = find_packages(where = 'denoiser'),
        package_data={'':[PACKAGE_DATA]},
        install_requires = REQUIREMENTS,
        
        classifiers = [
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9"
        ],
        
        keywords = ['audio denoise','denoise','cleanunet','speech denoise'],
        
        url = {
                'GitHub':GITHUB_URL,
                'Author':AUTHOR_WEBSITE
                },
)