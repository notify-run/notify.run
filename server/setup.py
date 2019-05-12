from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='notify-run-server',
      version='0.0.2',
      python_requires='>=3.6',
      description='Server for self-hosted notify.run server.',
      long_description=readme(),
      author='Paul Butler',
      author_email='notify@paulbutler.org',
      url='https://notify.run/',
      packages=['notify_run_server'],
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'notify-run-server = notify_run_server.app:main'
          ]
      },
      install_requires=[
          'PyQRCode==1.2.1',
          'cryptography>=2.5.0',
          'requests>=2.21.0',
          'Flask==1.0.2',
          'Flask-Cors==3.0.3',
          'SQLAlchemy>=1.3.0',
          'pywebpush==1.5.0',
          'setuptools>=41.0.1',
      ],
      )
