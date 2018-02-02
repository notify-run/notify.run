from setuptools import setup

setup(name='notify-run',
      version='0.0.1',
      description='Client for notify.run notifications.',
      author='Paul Butler',
      author_email='notify@paulbutler.org',
      url='https://notify.run/',
      packages=['notify_run'],
      entry_points={
          'console_scripts': [
              'notify-run = notify_run.cli:main'
          ]
      }
      )
