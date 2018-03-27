from .core import Chain, PBCChain, Square, PBCSquare
from .core import LatticeBase


__all__ = [
    'Chain',
    'PBCChain',
    'Square',
    'PBCSquare',
    'Lattice',
]


def Lattice(**kwargs):
    """Create a lattice.

    This is a factory method for creating lattice, eg. Chain, Square

    What is a factory method?

    Reference:

    http://python-3-patterns-idioms-test.readthedocs.io/en
    /latest/Factory.html#abstract-factories

    Shape:

        shape information is specified by `shape` keyword, if an
        alternative keyword is specified, keyword `name` will not
        be necessary.

        shape: this keyword is for general shape information
        length: for chain lattice, an alternative keyword can be used


    Lattice:

        Lattice type is specified by `name`.

    Others:

        Other parameters will not processed by this factory method. If it
        is required by desired lattice class, error will raise from the class
        initialization method.

    Raises:
        Raises TypeError when neither keyword name nor specified shape keyword
        is given.
        Raises ValueError when desired lattice is not implemented.

    Example:

    use `shape` and other lattice parameters to create a lattice
    `name` and `shape` is required, others could be optional.
    >>> Lattice(shape=(2, 4), pbc=True, name='Square')
    --> PBCSquare(shape=(2, 4), name='Square')

    if keyword `length` is given, it create a Chain lattice
    by default. Or `shape` will be required.
    >>> Lattice(length=4, pbc=True)
    --> PBCChain(length=4)
    """
    if 'name' in kwargs:
        name = kwargs.pop('name')
    else:
        name = None

    if 'length' in kwargs:
        kwargs.pop('name', None)
        name = 'Chain'

    if name is None:
        raise TypeError("lattice name is required")

    if 'pbc' in kwargs and kwargs.pop('pbc') is True:
        name = 'PBC' + name
    for cls in LatticeBase.__subclasses__():
        if cls.__name__.lower() == name.lower():
            return cls(**kwargs)
    raise ValueError("%s lattice is not implemented" % name)
