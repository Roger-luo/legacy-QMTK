# TODOs

## Architecture

- [ ] fine-tune
- [ ] ouput basis

## Sampler

- [x] add a direct sampler `STDirect`
- [ ] process safety

## Need fix

- [x] decorator did not wrap original docs
- [ ] test for this case

```python
h = J1J2(shape=(2, 2), pbc=True, J=(1.0, 1.0))
```

Default hamiltonian make a chain lattice, but this does not raises error, fixed now but more tests needed

## tomography

- [ ] example code needed (urgent!)
- [ ] quantum state class
- [x] quantum basis transformation (or use QuTiP?)


## Collector

- [ ] save
- [ ] load

## Hamiltonian

- [ ] keyword alias

## gradient check

- [ ] `utils.ground`
- [ ] `syn.grad.sr`

## dynamics

- [ ] `C` lib for adiabatic quantum computing

## tensor networks

- [ ] base class
- [ ] tensor contraction design doc

## Docs

- [x] collector
- [x] configs
- [x] ham
- [ ] others

## Others

- [ ] check and rewrite all function and methods with decorator `typecheck` and `alias`
