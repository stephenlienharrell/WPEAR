from setuptools import setup

setup(name='wpear',
      version='0.1',
      description='Weather Prediction Evaluation and Reporting',
      url='https://github.com/stephenlienharrell/WPEAR',
      author='Stephen Lien Harrell, Lala Vaishno De, Mengxue Luo, Dhairya Doshi',
      author_email='sharrell@purdue.edu',
      license='GPLv3',
      install_requires=['configargparse', 'pygrib', 'numpy', 'matplotlib', 'basemap'],
      packages=['wpear'],
      zip_safe=False)
