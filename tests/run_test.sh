#!/usr/bin/env bash
set -e

PYCMD=${PYCMD:="python"}
COVERAGE=0
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -p|--python) PYCMD=$2; shift 2 ;;
        -c|--coverage) COVERAGE=1; shift 1;;
        --) shift; break ;;
        *) echo "Invalid argument: $1!" ; exit 1 ;;
    esac
done

if [[ $COVERAGE -eq 1 ]]; then
    coverage erase
    PYCMD="coverage run --parallel-mode --source torch "
    echo "coverage flag found. Setting python command to: \"$PYCMD\""
fi

pushd "$(dirname "$0")"

echo "Running configurations tests"
$PYCMD test_configs.py $@

echo "Running collector tests"
$PYCMD test_collector.py $@

echo "Running sampler tests"
$PYCMD test_sampler.py $@

echo "Running lattice tests"
echo "TODO:"
echo "  * need tests for grid iterators"
$PYCMD test_lattice.py $@

echo "Running hamiltonian tests"
echo "TODO:"
echo "  * multi-threading tests and test suites"
echo "    this test is too slow"
$PYCMD test_ham.py $@

echo "Running basis tests"
$PYCMD test_basis.py $@


if [[ $COVERAGE -eq 1 ]]; then
    coverage combine
    coverage html
fi

popd
