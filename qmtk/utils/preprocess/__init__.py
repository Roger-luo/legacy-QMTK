from .base import Preprocessor
from .qmtk_loggers import log
from .qmtk_type_decorators import TypeCheck, Alias, Require
from .docs_processors import DocInherit

__all__ = [
    'Preprocessor',
    'TypeCheck',
    'typecheck',
    'DocInherit'
    'inheritdoc',
    'Alias',
    'alias',
    'Require',
    'require',
    'log',
]

# decorator alias
inheritdoc = DocInherit

for cls in Preprocessor.__subclasses__():
    exec(cls.__name__.lower() + ' = ' + cls.__name__)

del base
del qmtk_loggers
del qmtk_type_decorators
del docs_processors
