#!/usr/bin/env python

from setuptools import setup, find_packages, Command, distutils
import setuptools.command.install
import setuptools.command.develop
import setuptools.command.build_py
import distutils.command.build
import distutils.command.clean
import shutil
import subprocess
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class build_py(setuptools.command.build_py.build_py):

    def run(self):
        self.create_version_file()
        setuptools.command.build_py.build_py.run(self)

    @staticmethod
    def create_version_file():
        global version, cwd
        print('-- Building version ' + version)
        version_path = os.path.join(cwd, 'vmc', 'version.py')
        with open(version_path, 'w') as f:
            f.write("__version__ = '{}'\n".format(version))


class build_module(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('build_py')


class develop(setuptools.command.develop.develop):

    def run(self):
        build_py.create_version_file()
        setuptools.command.develop.develop.run(self)


class build(distutils.command.build.build):
    sub_commands = distutils.command.build.build.sub_commands


class install(setuptools.command.install.install):

    def run(self):
        # if not self.skip_build:
        #     self.run_command('build_deps')
        setuptools.command.install.install.run(self)


class clean(distutils.command.clean.clean):

    def run(self):
        import glob
        with open('.gitignore', 'r') as f:
            ignores = f.read()
            for wildcard in filter(bool, ignores.split('\n')):
                for filename in glob.glob(wildcard):
                    try:
                        os.remove(filename)
                    except OSError:
                        shutil.rmtree(filename, ignore_errors=True)

        # It's an old-style class in Python 2.7...
        distutils.command.clean.clean.run(self)


cwd = os.path.dirname(os.path.abspath(__file__))

version = '0.0.1'
if os.getenv('PYVMC_BUILD_VERSION'):
    assert os.getenv('PYVMC_BUILD_NUMBER') is not None
    version = os.getenv('PYVMC_BUILD_VERSION') \
        + '_' + os.getenv('PYVMC_BUILD_NUMBER')
else:
    try:
        sha = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=cwd).decode('ascii').strip()
        version += '+' + sha[:7]
    except subprocess.CalledProcessError:
        pass

packages = find_packages()

setup(name="vmc", version=version,
      description="Variational Monte Carlo Package",
      cmdclass={
          'build': build,
          'build_py': build_py,
          'build_module': build_module,
          'develop': develop,
          'install': install,
          'clean': clean,
      },
      packages=packages,
      install_requires=['pyyaml', 'numpy', 'scipy'],
      )


# setup(
#     name="vmc",
#     version="0.0.1",
#     author="Roger Luo",
#     author_email="rogerluo.rl18@gmail.com",
#     description=("Variational Monte Carlo Package"),
#     license="MIT",
#     keywords="Monte Carlo",
#     url="http://packages.python.org/an_example_pypi_project",
#     packages=['vmc', 'vmc/configs', 'vmc/collector/'],
#     long_description=read('README.md'),
#     classifiers=[
#         "Development Status :: 2 - Pre-Alpha",
#         'Intended Audience :: Developers',
#         'Intended Audience :: Science/Research',
#         'License :: OSI Approved :: MIT',
#         'Topic :: Scientific/Engineering',
#         'Topic :: Software Development',
#         'Operating System :: Microsoft :: Windows',
#         'Operating System :: POSIX',
#         'Operating System :: Unix',
#         'Operating System :: MacOS',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.3',
#     ],
#     install_requires=['numpy', 'scipy'],
# )
