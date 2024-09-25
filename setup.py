from setuptools import setup, find_packages
import pip

NAME = 'audio-denoiser'
VERSION = '0.0.0.dev1' 
DESCRIPTION = 'CleanUNet based audio denoiser'
GITHUB_URL = 'https://github.com/Kabir5296/Audio-Denoiser.git'

AUTHOR = "A F M Mahfuzul Kabir"
AUTHOR_EMAIL = "<afmmahfuzulkabir@gmail.com>"

REQUIREMENTS = open('requirements.txt').read().splitlines()
README = open('README.md').read()

setup(
        name = NAME, 
        version = VERSION,
        
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        description = DESCRIPTION,
        long_description = README,
        long_description_content_type = 'text/markdown',
        packages = find_packages(where = 'denoiser'),
        install_requires = REQUIREMENTS,
        
        classifiers = [
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9"
        ],
        
        keywords = ['audio denoise','denoise','cleanunet','speech denoise'],
        
        url = GITHUB_URL,
)