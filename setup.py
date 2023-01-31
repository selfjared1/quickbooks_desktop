from distutils.core import setup

setup(
    name='quickbooks_desktop',
    packages=['quickbooks_desktop'],
    version='1.0.1',  # Ideally should be same as your GitHub release tag version
    description='Initial Release',
    author='Jared Self',
    author_email='jared@quickbooksgg.com',
    url='https://github.com/selfjared1/syncfreedom-lib/releases/tag/0.1',
    download_url='https://github.com/selfjared1/syncfreedom-lib/archive/refs/tags/0.1.zip',
    keywords=['quickbooks online', 'quickbooks'],
    classifiers=[],
    install_requires=[
        'python-quickbooks'
    ]
)