from setuptools import setup

setup(
    name='AWSAutomate',
    version='0.1',
    author='Milton Ellison',
    description='Tool used to deploy static websites to aws',
    license='GPLv3+',
    packages=['Script'],
    url='https://github.com/Mdot23/AWS_Automation',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        aws_automate=Script.CLI:cli
    '''
)
