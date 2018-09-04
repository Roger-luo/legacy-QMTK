Configs
===================================
.. automodule:: vmc.configs

vmc.configs
===================================

configs are subclass of :class:`GeneratorBase`, configs implements quantum configuration generation methods:

    automethod:: step
    automethod:: sample

There are some other methods that may not need to be modified:

    automethod:: measure

Currently, sampling methods below is implemented:

    :class: `STMetropolis` Single thread metropolis
    :class: `MPMetropolis` Multi - process metropolis
    :class: `Metropolis` an unified API for metropolis method


