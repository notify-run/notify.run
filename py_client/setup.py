from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='notify-run',
      version='0.0.12',
      python_requires='>=2.7',
      description='Client for notify.run notifications.',
      long_description=readme(),
      author='Paul Butler',
      author_email='notify@paulbutler.org',
      url='https://notify.run/',
      packages=['notify_run'],
      entry_points={
          'console_scripts': [
              'notify-run = notify_run.cli:main'
          ]
      },
      install_requires=[
          'PyQRCode==1.2.1',
          'requests==2.20.0',
      ],
      )
