from setuptools import setup, Extension, find_packages, Command, distutils
import setuptools.command.build_ext
import setuptools.command.install
import setuptools.command.develop
import setuptools.command.build_py
import distutils.unixccompiler
import distutils.command.build
import distutils.command.clean
import distutils.ccompiler
import os
import sys
import subprocess
import platform
import shutil


def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.
    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler -- at least C++11 support '
                           'is needed!')


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
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    if sys.platform == 'darwin':
        c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    def run(self):
        setuptools.command.build_ext.build_ext.run(self)

    # def build_extensions(self):
    #     ct = self.compiler.compiler_type
    #     opts = self.c_opts.get(ct, [])
    #     if ct == 'unix':
    #         opts.append('-DVERSION_INFO="%s"' %
    #                     self.distribution.get_version())
    #         opts.append(cpp_flag(self.compiler))
    #         if has_flag(self.compiler, '-fvisibility=hidden'):
    #             opts.append('-fvisibility=hidden')
    #     elif ct == 'msvc':
    #         opts.append('/DVERSION_INFO=\\"%s\\"' %
    #                     self.distribution.get_version())
    #     for ext in self.extensions:
    #         ext.extra_compile_args = opts
    #     build_ext.build_extensions(self)


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
extra_compile_args = ['-std=c++14', '-O3',
                      '-Wno-write-strings']

cwd = os.path.dirname(os.path.abspath(__file__))

include_dirs += [
    cwd,
    os.path.join(sys.exec_prefix, 'include'),
]

main_compile_args = ['-D_CORE']
main_libraries = []
main_link_args = []
main_sources = [
    'qmtk/csrc/lattice.cpp'
]


lattice = Extension('qmtk._lattice',
                    sources=main_sources,
                    libraries=main_libraries,
                    language='c++',
                    extra_compile_args=main_compile_args + extra_compile_args,
                    include_dirs=include_dirs,
                    library_dirs=library_dirs,
                    extra_link_args=extra_link_args +
                    main_link_args,
                    )

utils = Extension('qmtk._utils',
                  sources=['qmtk/csrc/utils.cpp'],
                  libraries=main_libraries,
                  language='c++',
                  extra_compile_args=main_compile_args + extra_compile_args,
                  include_dirs=include_dirs,
                  library_dirs=library_dirs,
                  extra_link_args=extra_link_args +
                  main_link_args,
                  )

space = Extension('qmtk._space',
                  sources=['qmtk/csrc/space.cpp'],
                  libraries=main_libraries,
                  language='c++',
                  extra_compile_args=main_compile_args + extra_compile_args,
                  include_dirs=include_dirs,
                  library_dirs=library_dirs,
                  extra_link_args=extra_link_args +
                  main_link_args,
                  )

ham = Extension('qmtk._ham',
                sources=['qmtk/csrc/ham.cpp'],
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
    ext_modules=[lattice, utils, space, ham],
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
    test_suite='test',
)
