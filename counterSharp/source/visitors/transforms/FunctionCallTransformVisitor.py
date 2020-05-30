# TODO: Transform every function call
# If used as expression: Must be moved up and stored in temporary variable
# This must only happen for "known" functions (i.e. encountered in some file)
# Therefore a function register must be constructed containing the return types of any function
# We might want to move the "if condition broken true compound statement" up in the class hirachy so it can be used by this visitor as well...
# How to handle function pointers? (i.e. how do wo know their return type?)
# Index of function identifiers?
# We should definetly do a check after those ones...