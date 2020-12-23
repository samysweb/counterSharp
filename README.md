# counterSharp
A tool allowing the quantification of software properties through Model Counting: We use [CBMC](http://www.cprover.org/cbmc/) to transform C-code into SAT instances and then run (approximate) model counting (e.g. [ApproxMC](https://github.com/meelgroup/ApproxMC)) on those instances.

## Installation
- Tested with Python 3.8 and CBMC 5.11
- Expects CBMC and cpp (C preprocessing) to be in PATH
- Expects `requirements.txt` to be installed through pip (specifically we are using [pycparser](https://github.com/eliben/pycparser))
- Alternatively available in a [Docker Container](#Docker-Guide)

## Usage
Run counterSharp as:
```
python -m counterSharp -amm <assume miss dimacs> --amh <assume hit dimacs> --asm <assert miss dimacs> --ash <assert hit dimacs> <inputfiles...>
```

counterSharp will read and transform the input files and use CBMC to produce 4 dimacs files on which model counting can be applied by tools like ApproxMC.

## Additional Paramters
Frequently helpful:
Parameter | Description
---|---
`-h, --help` | Show help message and exit
`-d` | Debug Mode (more output)
`--function <fun>` | Name of the function to be analyze
`--cbmcArg <args>` | Additional input paramters for CBMC
`--unwindDepth <depth>` | The unwind depth of CBMC (otherwise found through iteration over depths)

The default for `--function` is main. Splicing must explictly be activated for CBMC.

Less frequently helpful:
Parameter | Description
---|---
`--assertMissVar <name>` | Name of the assert miss state variable
`--assumeMissVar <name>` | Name of the assume miss state variable
`--assertFunction <name>` | Name of the assert function
`--assumeFunction <name>` | Name of the assume function
`--returnLabel <name>` | Name of the return label

All these are set to default values which are unlikely to clash with your code unless you use variables/functions/labels which begin with `__counterSharp_`

## Docker Guide


## Why counterSharp?
> counterSharp counts (thus sharp/#) counterexamples (thus counter) for a given specification.