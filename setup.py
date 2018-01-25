from setuptools import setup, Extension, find_packages, Command, distutils
import setuptools.command.build_ext
import setuptools.command.install
import setuptools.command.develop
import setuptools.command.build_py
import distutils.unixccompiler
import distutils.command.build
import distutils.command.clean
import os
import subprocess
import platform
import shutil


class build_module(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('build_py')
        self.run_command('build_ext')


class build_py(setuptools.command.build_py.build_py):

    def run(self):
        self.create_version_file()
        setuptools.command.build_py.build_py.run(self)

    @staticmethod
    def create_version_file():
        global version, cwd
        print('-- Building version ' + version)
        version_path = os.path.join(cwd, 'qmtk', 'version.py')
        with open(version_path, 'w') as f:
            f.write("__version__ = '{}'\n".format(version))


class develop(setuptools.command.develop.develop):

    def run(self):
        build_py.create_version_file()
        setuptools.command.develop.develop.run(self)


class build_ext(setuptools.command.build_ext.build_ext):

    def run(self):
        setuptools.command.build_ext.build_ext.run(self)


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

        distutils.command.clean.clean.run(self)


def make_relative_rpath(path):
    if platform.system() == 'Darwin':
        return '-Wl,-rpath,@loader_path/' + path
    else:
        return '-Wl,-rpath,$ORIGIN/' + path


include_dirs = []
library_dirs = []
extra_link_args = []
extra_compile_args = ['-std=c++11', '-O3', '-Wno-write-strings']

cwd = os.path.dirname(os.path.abspath(__file__))

include_dirs += [
    cwd,
]

main_compile_args = ['-D_CORE']
main_libraries = []
main_link_args = []
main_sources = [
    'qmtk/lattice/csrc/lattice.cpp'
]


clattice = Extension('qmtk._lattice',
                     sources=main_sources,
                     libraries=main_libraries,
                     language='c++',
                     extra_compile_args=main_compile_args + extra_compile_args,
                     include_dirs=include_dirs,
                     library_dirs=library_dirs,
                     extra_link_args=extra_link_args +
                     main_link_args,
                     )

version = '0.1.12'
if os.getenv('PYTORCH_BUILD_VERSION'):
    assert os.getenv('PYTORCH_BUILD_NUMBER') is not None
    version = os.getenv('PYTORCH_BUILD_VERSION') \
        + '_' + os.getenv('PYTORCH_BUILD_NUMBER')
else:
    try:
        sha = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=cwd).decode('ascii').strip()
        version += '+' + sha[:7]
    except subprocess.CalledProcessError:
        pass

setup(
    name='qmtk',
    version='0.1',
    description='quantum mechanics toolkit',
    ext_modules=[clattice],
    cmdclass={
        'build_py': build_py,
        'build_ext': build_ext,
        'build_module': build_module,
        'develop': develop,
        'clean': clean,
    },
    packages=find_packages(),
    package_data={'qmtk': [
        'lib/*.so',
        'lib/*.hpp',
    ]},
)
