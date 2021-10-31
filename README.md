# counterSharp
A tool allowing the quantification of software properties through Model Counting: We use [CBMC](http://www.cprover.org/cbmc/) to transform C-code into SAT instances and then run (approximate) model counting (e.g. [ApproxMC](https://github.com/meelgroup/ApproxMC)) on those instances.

## Installation
- Tested with Python 3.8 and CBMC 5.11
- Expects CBMC and cpp (C preprocessing) to be in PATH
- Expects `requirements.txt` to be installed through pip (specifically we are using [pycparser](https://github.com/eliben/pycparser))

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
`--smt2` | Returns (customized) SMT-LIB2 files instead of DIMACS files (see SMT section)

All these are set to default values which are unlikely to clash with your code unless you use variables/functions/labels which begin with `__counterSharp_`
### Obtaining SMT files
**Warning:** The SMT-LIB functionality should still be considered experimental, as it is not as well tested as the DIMACS output!

Instead of providing DIMACS files, counterSharp can also provide SMT files.
These files are also generated through CBMC, but with its SMT-LIB2 backend.
Just as for DIMACS files, these files contain specific projection information:
- If a variable is supposed to be used for projection this is indicated through:  
	```
	(project-on varname)
	```
- Instead of a `(check-sat)` instruction, there will be a `(count-sat)` operation
- Any `(get-value ...)` instructions are suppressed, as this doesn't make sense in the case of counting

## Why counterSharp?
> counterSharp counts (thus sharp/#) counterexamples (thus counter) for a given specification.