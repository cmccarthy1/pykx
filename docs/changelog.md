# Changelog

## PyKX 1.6.1

### Additions

- Added `sorted`, `grouped`, `parted`, and `unique`. As methods off of `Tables` and `Vectors`.
- Added `PyKXReimport` class to allow subprocesses to reimport `PyKX` safely.
    - Also includes `.pykx.safeReimport` in `pykx.q` to allows this behaviour when running under q as well.
- Added environment variables to specify a path to `libpython` in the case `pykx.q` cannot find it.

### Fixes and Improvements

- Fixed memory leaks within the various `QConnection` subclasses.
- Added deprecation warning around the discontinuing of support for Python 3.7.
- Fixed bug in Jupyter Notebook magic command.
- Fixed a bug causing `np.ndarray`'s to not work within `ufuncs`.
- Fixed a memory leak within all `QConnection` subclasses. Fixed for both `PyKX` as a client and as a server.
- Updated insights libraries to 4.0.2
- Fixed `pykx.q` functionality when run on Windows.
- Fixed an issue where reimporting `PyKX` when run under q would cause a segmentation fault.
- Updated the warning message for the insights core libraries failing to load to make it more clear that no error has occured.

## PyKX 1.6.0

### Additions

- Added `merge_asof` to the Pandas like API.
    - See [here](https://code.kx.com/pykx/user-guide/advanced/Pandas_API.html#tablemerge_asof) for details of supported keyword arguments and limitations.
- Added `set_index` to the Pandas like API.
    - See [here](https://code.kx.com/pykx/user-guide/advanced/Pandas_API.html##setting-indexes) for details of supported keyword arguments and limitations.
- Added a set of basic computation methods operating on tabular data to the Pandas like API. See [here](https://code.kx.com/pykx/user-guide/advanced/Pandas_API.html#computations) for available methods and examples.
- `pykx.util.debug_environment` added to help with import errors.
- q vector type promotion in licensed mode.
- Added `.pykx.toraw` to `pykx.q` to enable raw conversions (e.g. `kx.toq(x, raw=True)`)
- Added support for Python `3.11`.
    - Support for pyarrow in this python version is currently in Beta.
- Added the ability to use `kx.RawQConnection` as a Python based `q` server using `kx.RawQConnection(port=x, as_server=True)`.
    - More documentation around using this functionality can be found [here](examples/server/server.html).

### Fixes and Improvements

- Improved error on Windows if `msvcr100.dll` is not found
- Updated q libraries to 2023.04.17
- Fixed an issue that caused `q` functions that shared a name with python key words to be inaccessible using the context interface.
    - It is now possible to access any `q` function that uses a python keyword as its name by adding an underscore to the name (e.g. `except` can now be accessed using `q.except_`).
- Fixed an issue with `.pykx.get` and `.pykx.getattr` not raising errors correctly.
- Fixed an issue where `deserializing` data would sometimes not error correctly.
- Users can now add new column(s) to an in-memory table using assignment when using the Pandas like API.

	```python
	>>> import os
	>>> os.environ['PYKX_ENABLE_PANDAS_API'] = 'true'
	>>> import pykx as kx
	>>> import numpy as np
	>>> tab = kx.q('([]100?1f;100?1f)')
	>>> tab['x2'] = np.arange(0, 100)
	>>> tab
	pykx.Table(pykx.q('
	x           x1         x2
	-------------------------
	0.1485357   0.1780839  0
	0.4857547   0.3017723  1
	0.7123602   0.785033   2
	0.3839461   0.5347096  3
	0.3407215   0.7111716  4
	0.05400102  0.411597   5
	..
	'))
	```

## PyKX 1.5.3

### Additions

- Added support for Pandas `Float64Index`.
- Wheels for ARM64 based Macs are now available for download.

## PyKX 1.5.2

### Additions

- Added support for ARM 64 Linux.

## PyKX 1.5.1

### Fixes and Improvements

- Fixed an issue with `pykx.q` that caused errors to not be raised properly under q.
- Fixed an issue when using `.pykx.get` and `.pykx.getattr` that caused multiple calls to be made.

## PyKX 1.5.0

### Additions

- Added wrappers around various `q` [system commands](https://code.kx.com/q/basics/syscmds/).
- Added `merge` method to tables when using the `Pandas API`.
- Added `mean`/`median`/`mode` functions to tables when using the `Pandas API`.
- Added various functions around type conversions on tables when using the `Pandas API`.

### Fixes and Improvements

- Fix to allow GUIDs to be sent over IPC.
- Fix an issue related to IPC connection using compression.
- Improved the logic behind loading `pykx.q` under a `q` process allowing it to run on MacOS and Linux in any environment that `EmbedPy` works in.
- Fix an issue that cause the default handler for `SIGINT` to be overwritten.
- `pykx.toq.from_callable` returns a `pykx.Composition` rather than `pykx.Lambda`. When executed returns an unwrapped q object.
- Fixed conversion of Pandas Timestamp objects.
- Fixed an issue around the `PyKX` `q` magic command failing to load properly.
- Fixed a bug around conversions of `Pandas` tables with no column names.
- Fixed an issue around `.pykx.qeval` not returning unwrapped results in certain scenarios.

## PyKX 1.4.2

### Fixes and Improvements

- Fixed an issue that would cause `EmbeddedQ` to fail to load.

## PyKX 1.4.1

### Fixes and Improvements

- Added constructors for `Table` and `KeyedTable` objects to allow creation of these objects from dictionaries and list like objects.
- Fixed a memory leak around calling wrapped `Foreign` objects in `pykx.q`.
- Fixed an issue around the `tls` keyword argument when creating `QConnection` instances, as well as a bug in the unlicensed behaviour of `SecureQConnection`'s.

## PyKX 1.4.0

### Additions

- Addition of a utility function `kx.ssl_info()` to retrieve the SSL configuration when running in unlicensed mode (returns the same info as kx.q('-26!0') with a license).
- Addition of a utility function `kx.schema.builder` to allow for the generation of `pykx.Table` and `pykx.KeyedTable` types with a defined schema and zero rows, this provides an alternative to writing q code to create an empty table.
- Added helper functions for inserting and upserting to `k.Table` instances. These functions provide new keyword arguments to run a test insert against the table or to enforce that the schema of the new row matches the existing table.
- Added environment variable `PYKX_NOQCE=1` to skip the loading of q Cloud Edition in order to speed up the import of PyKX.
- Added environment variable `PYKX_LOAD_PYARROW_UNSAFE=1` to import PyAarrow without the "subprocess safety net" which is here to prevent some hard crashes (but is slower than a simple import).
- Addition of method `file_execute` to `kx.QConnection` objects which allows the execution of a local `.q` script on a server instance as outlined [here](user-guide/advanced/ipc.md#file_execution).
- Added `kx.RawQConnection` which extends `kx.AsyncQConnection` with extra functions that allow a user to directly poll the send and receive selectors.
- Added environment variable `PYKX_RELEASE_GIL=1` to drop the [`Python GIL`](https://wiki.python.org/moin/GlobalInterpreterLock) on calls into embedded q.
- Added environment variable `PYKX_Q_LOCK=1` to enable a Mutex Lock around calls into q, setting this environment variable to a number greater than 0 will set the max length in time to block before raising an error, a value of '-1' will block indefinitely and will not error, any other value will cause an error to be raised immediately if the lock cannot be acquired.
- Added `insert` and `upsert` methods to `Table` and `KeyedTable` objects.

### Fixes and Improvements

- Fixed `has_nulls` and `has_infs` properties for subclasses of `k.Collection`.
- Improved error output of `kx.QConnection` objects when an error is raised within the context interface.
- Fixed `.py()` conversion of nested `k.Dictionary` objects and keyed `k.Dictionary` objects.
- Fixed unclear error message when querying a `QConnection` instance that has been closed.
- Added support for conversions of non C contiguous numpy arrays.
- Fixed conversion of null `GUIDAtom`'s to and from numpy types.
- Improved performance of converting `q` enums to pandas Categoricals.

### Beta Features

- Added support for a Pandas like API around `Table` and `KeyedTable` instances, documentation for the specific functionality can be found [here](user-guide/advanced/Pandas_API.ipynb).
- Added `.pykx.setdefault` to `pykx.q` which allows the default conversion type to be set without using environment variables.

## PyKX 1.3.2

### Features and Fixes

- Fixed support for using TLS with `SyncQConnection` instances.

## PyKX 1.3.1

### Features and Fixes

- Added environment variable `PYKX_Q_LIB_LOCATION` to specify a path to load the PyKX q libraries from.
    - Required files in this directory
        - If you are using the kdb+/q Insights core libraries they all must be present within this folder.
        - The `read.q`, `write.q`, and `csvutil.q` libraries that are bundled with PyKX.
        - A `q.k` that matches the version of `q` you are loading.
        - There must also be a subfolder (`l64` / `m64` / `w64`) based on the platform you are using.
            - Within this subfolder a copy of these files must also be present.
                - `libq.(so / dylib)` / `q.dll`.
                - `libe.(so / dylib)` / `e.dll`.
                - If using the Insights core libraries their respective shared objects must also be present here.
- Updated core q libraries
    - PyKX now supports M1 Macs
    - OpenSSLv3 support
- Added ability to specify maximum length for IPC error messages. The default is 256 characters and this can be changed by setting the `PYKX_MAX_ERROR_LENGTH` environment variable.

## PyKX 1.3.0

### Features and Fixes

- Support for converting `datetime.datetime` objects with timezone information into `pykx.TimestampAtom`s and `pykx.TimestampVector`s.
- Added a magic command to run cells of q code in a Jupyter Notebook. The addition of `%%q` at the start of a Jupyter Notebook cell will allow a user to execute q code locally similarly to loading a q file.
- Added `no_ctx` key word argument to `pykx.QConnection` instances to disable sending extra queries to/from q to manage the context interface.
- Improvements to SQL interface for PyKX including the addition of support for prepared statements, execution of these statements and retrieval of inputs see [here](api/query.md#pykx.query.SQL) for more information.
- Fix to memory leak seen when converting Pandas Dataframes to q tables.
- Removed unnecessary copy when sending `q` objects over IPC.

### Beta Features

- EmbedPy replacement functionality `pykx.q` updated significantly to provide parity with embedPy from a syntax perspective. Documentation of the interface [here](api/pykx_under_q.md) provides API usage. Note that initialisation requires the first version of Python to be retrieved on a users `PATH` to have PyKX installed. Additional flexibility with respect to installation location is expected in `1.4.0` please provide any feedback to `pykx@kx.com`

## PyKX 1.2.2

### Features and Fixes

- Fixed an issue causing the timeout argument for `QConnection` instances to not work work properly.

## PyKX 1.2.1

### Features and Fixes

- Added support for OpenSSLv3 for IPC connections created when in 'licensed' mode.
- Updated conversion functionality for timestamps to support conversions within Pandas 1.5.0

## PyKX 1.2.0

### Features and Fixes

- Support for converting any python type to a `q` Foreign object has been added.
- Support for converting Pandas categorical types into `pykx.EnumVector` type objects.
- Support for q querying against Pandas/PyArrow tables through internal conversion to q representation and subsequent query. `kx.q.qsql.select(<pd.DataFrame>)`
- Support for casting Python objects prior to converting into K objects. (e.g. `kx.IntAtom(3.14, cast=True)` or `kx.toq("3.14", ktype=kx.FloatAtom, cast=True)`).
- Support usage of numpy [`__array_ufunc__`'s](https://numpy.org/doc/stable/reference/ufuncs.html) directly on `pykx.Vector` types.
- Support usage of numpy `__array_function__`'s directly on `pykx.Vector` types (Note: these will return a numpy ndarray object not an analogous `pykx.K` object).
- Improved performance of `pykx.SymbolVector` conversion into native Python type (e.g. `.py()` conversion for `pykx.SymbolVector`'s).
- Improved performance and memory usage of various comparison operators between `K` types.
- Improved performance of various `pykx.toq` conversions.
- `pykx.Vector` types will now automatically enlist atomic types instead of erroring.
- Fixed conversions of numpy float types into `pykx.FloatAtom` and `pykx.RealAtom` types.
- Fixed conversion of `None` Python objects into analogous null `K` types if a `ktype` is specified.
- Added `event_loop` parameter to `pykx.AsyncQConnection` that takes a running event loop as a parameter and allows the event loop to manage `pykx.QFuture` objects.

### Beta Features

- Added extra functionality to `pykx.q` related to the calling and use of python foreign objects directly within a `q` process.
- Support for [NEP-49](https://numpy.org/neps/nep-0049.html), which allows numpy arrays to be converted into `q` Vectors without copying the underlying data. This behaviour is opt-in and you can do so by setting the environment variable `PYKX_ALLOCATOR` to 1, "1" or True or by adding the flag `--pykxalloc` to the `QARGS` environment variable. Note: This feature also requires a python version of at least 3.8.
- Support the ability to trigger early garbage collection of objects in the `q` memory space by adding `--pykxgc` to the QARGS environment variable, or by setting the `PYKX_GC` environment variable to 1, "1" or True.

## PyKX 1.1.1

### Features & Fixes

- Added ability to skip symlinking `$QHOME` to `PyKX`'s local `$QHOME` by setting the environment variable `IGNORE_QHOME`.

## PyKX 1.1.0

### Dependencies

- The dependency on the system library `libcurl` has been made optional for Linux. If it is missing on Linux, a warning will be emitted instead of an error being raised, and the KX Insights Core library `kurl` will not be fully loaded. Windows and macOS are unaffected, as they don't support the KX Insights Core features to begin with.

### Features & Fixes

- Splayed and partitioned tables no longer emit warnings when instantiated.
- Added `pykx.Q.sql`, which is a wrapper around [KXI Core SQL](https://code.kx.com/insights/core/sql.html#sql-language-support).
- `.pykx.pyexec` and `.pykx.pyeval` no longer segfault when called with a character atom.
- Updated several `pykx.toq` tests so that they would not randomly fail.
- Fixed error when pickling `pykx.util.BlockManager` in certain esoteric situations.
- Fixed `pandas.MultiIndex` objects created by PyKX having `pykx.SymbolAtom` objects within them - now they have `str` objects instead, as they normally would.
- Upgraded the included KX Insights Core libraries to version 3.0.0.
- Added `pykx.toq.from_datetime_date`, which converts `datetime.date` objects into any q temporal atom that can represent a date (defaulting to a date atom).
- Fixed error when user specifies `-s` or `-q` in `$QARGS`.
- Fixed recursion error when accessing a non-existent attribute of `pykx.q` while in unlicensed mode. Now an attribute error is raised instead.
- Fixed build error introduced by new rules enforced by new versions of setuptools.
- Added `pykx.Anymap`.
- Fixed support for `kx.lic` licenses.
- The KXIC libraries are now loaded after q has been fully initialized, rather than during the initialization. This significantly reduces the time it takes to import PyKX.
- PyKX now uses a single location for `$QHOME`: its `lib` directory within the installed package. The top-level contents of the `$QHOME` directory (prior to PyKX updating the env var when embedded q is initialized) will be symlinked into PyKX's `lib` directory, along with the content of any subdirectories under `lib` (e.g. `l64`, `m64`, `w64`). This enables loading scripts and libraries located in the original `$QHOME` directory during q initialization.
- Improved performance (both execution speed and memory usage) of calling `np.array` on `pykx.Vector` instances. The best practice is still to use the `np` method instead of calling `np.array` on the `pykx.Vector` instance.
- `pykx.Vector` is now a subclass of `collections.abc.Sequence`.
- `pykx.Mapping` is not a subclass of `collections.abc.Mapping`.
- Split `pykx.QConnection` into `pykx.SyncQConnection` and `pykx.AsyncQConnection` and added support for asynchronous IPC with `q` using `async`/`await`. Refer to [the `pykx.AsyncQConnection` docs](api/ipc.md#pykx.ipc.AsyncQConnection) for more details.
- Pandas dataframes containing Pandas extension arrays not originally created as Numpy arrays would result in errors when attempting to convert to q. For example a Dataframe with index of type `pandas.MultiIndex.from_arrays` would result in an error in conversion.
- Improved performance of converting `pykx.SymbolVector` to `numpy.array` of strings, and also the conversion back from a `numpy.array` of `strings` to a `q` `SymbolVector`.
- Improved performance of converting `numpy.array`'s of `dtype`s `datetime64`/`timedelta64 ` to the various `pykx.TemporalTypes`.

## PyKX 1.0.1

### Deprecations & Removals

- The `sync` parameter for `pykx.QConnection` and `pykx.QConnection.__call__` has been renamed to the less confusing name `wait`. The `sync` parameter remains, but its usage will result in a `DeprecationWarning` being emitted. The `sync` parameter will be removed in a future version.

### Features & Fixes
- Updated to stable classifier (`Development Status :: 5 - Production/Stable`) in project metadata. Despite this update being done in version 1.0.1, version 1.0.0 is still the first stable release of PyKX.
- PyKX now provides source distributions (`sdist`). It can be downloaded from PyPI using `pip download --no-binary=:all: --no-deps pykx`. As noted in [the installation docs](getting-started/installing.md#supported-environments), installations built from the source will only receive support on a best-effort basis.
- Fixed Pandas NaT conversion to q types. Now `pykx.toq(pandas.NaT, ktype=ktype)` produces a null temporal atom for any given `ktype` (e.g. `pykx.TimeAtom`).
- Added [a doc page for limitations of embedded q](user-guide/advanced/limitations.md).
- Added a test to ensure large vectors are correctly handled (5 GiB).
- Always use synchronous queries internally, i.e. fix `QConnection(sync=False)`.
- Disabled the context interface over IPC. This is a temporary measure that will be reversed once q function objects are updated to run in the environment they were defined in by default.
- Reduced the time it takes to import PyKX. There are plans to reduce it further, as `import pykx` remains fairly slow.
- Updated to [KXI Core 2.1](https://code.kx.com/insights/core/release-notes/2.1.0.html) & rename `qce` -> `kxic`.
- Misc test updates.
- Misc doc updates.

## PyKX 1.0.0

### Migration Notes

To switch from Pykdb to PyKX, you will need to update the name of the dependency from `pykdb` to `pykx` in your `pyproject.toml`/`requirements.txt`/`setup.cfg`/etc. When Pykdb was renamed to PyKX, its version number was reset. The first public release of PyKX has the version number 1.0.0, and will employ [semantic versioning](https://semver.org/).

Pay close attention to the renames listed below, as well as the removals. Many things have been moved to the top-level, or otherwise reorganized. A common idiom with Pykdb was the following:

```python
from pykdb import q, k
```

It is recommended that the following be used instead:

```python
import pykx as kx
```

This way the many attributes at the top-level can be easily accessed without any loss of context, for example:

```python
kx.q # Can be called to execute q code
kx.K # Base type for objects in q; can be used to convert a Python object into a q type
kx.SymbolAtom # Type for symbol atoms; can be used to convert a `str` or `bytes` into a symbol atom
kx.QContext # Represents a q context via the PyKX context interface
kx.QConnection # Can be called to connect to a q process via q IPC
kx.PyKXException # Base exception type for exceptions specific to PyKX and q
kx.QError # Exception type for errors that occur in q
kx.LicenseException # Exception type raised when features that require a license are used without
kx.QHOME # Path from which to load q files, set by $QHOME environment variable
kx.QARGS # List of arguments provided to the embedded q instance at startup, set by $QARGS environment variable
# etc.
```

You can no longer rely on the [context](api/ctx.md) being reset to the global context after each call into embedded q, however IPC calls are unaffected.

### Renames
- Pykdb has been renamed to PyKX. `Pykdb` -> `PyKX`; `PYKDB` -> `PYKX`; `pykdb` -> `pykx`.
- The `adapt` module has been renamed to `toq`, and it can be called directly. Instead of `pykdb.adapt.adapt(x)` one should write `pykx.toq(x)`.
- The `k` module has been renamed to `wrappers`. All wrapper classes can be accessed from the top-level, i.e. `pykx.K`, `pykx.SymbolAtom`, etc.
- The "module interface" (`pykdb.module_interface`) has been renamed to the "context interface" (`pykx.ctx`). All `pykx.Q` instances (i.e. `pykx.q` and all `pykx.QConnection` instances) have a `ctx` attribute, which is the global `QContext` for that `pykx.Q` instance. Usually, one need not directly access the global context. Instead, one can access its subcontexts directly e.g. `q.dbmaint` instead of `q.ctx.dbmaint`.
- `KdbError` (and its subclasses) have been renamed to `QError`
- `pykdb.ctx.KdbContext` has been renamed to `pykx.ctx.QContext`, and is available from the top-level, i.e. `pykx.QContext`.
- The `Connection` class in the IPC module has been renamed to `QConnection`, and is now available at the top-level, i.e. `pykx.QConnection`.
- The q type wrapper `DynamicLoad` has been renamed to `Foreign` (`pykdb.k.DynamicLoad` -> `pykx.Foreign`).

### Deprecations & Removals
- The `pykdb.q.ipc` attribute has been removed. The IPC module can be accessed directly instead at `pykx.ipc`, but generally one will only need to access the `QConnection` class, which can be accessed at the top-level: `pykx.QConnection`.
- The `pykdb.q.K` attribute has been removed. Instead, `K` types can be used as constructors for that type by leveraging the `toq` module. For example, instead of `pykdb.q.K(x)` one should write `pykx.K(x)`. Instead of `pykx.q.K(x, k_type=pykx.k.SymbolAtom)` one should write `pykx.SymbolAtom(x)` or `pykx.toq(x, ktype=pykx.SymbolAtom)`.
- Most `KdbError`/`QError` subclasses have been removed, as identifying them is error prone, and we are unable to provide helpful error messages for most of them.
- The `pykx.kdb` singleton class has been removed.

### Dependencies
- More Numpy, Pandas, and PyArrow versions are supported. Current `pandas~=1.0`, `numpy~=1.20,<1.22`, and `pyarrow>=3.0.0` are supported. PyArrow remains an optional dependency.
- A dependency on `find-libpython~=0.2` was added. This is only used when running PyKX under a q process (see details in the section below about new alpha features).
- A dependency on the system library `libcurl` was added for Linux. This dependency will be made optional in a future release.

### Features & Fixes
- The `pykx.Q` class has been added as the base class for `pykx.EmbeddedQ` (the class for `pykx.q`) and `pykx.QConnection`.
- The `pykx.EmbeddedQ` process now persists its [context](api/ctx.md) between calls.
- The console now works over IPC.
- The query module now works over IPC. Because `K` objects hold no reference to the `q` instance that created them (be it local or over IPC), `K` tables no longer have `select`/`exec`/`update`/`delete` methods with themselves projected in as the first argument. That is to say, instead of writing `t.select(...)`, write `q.qsql.select(t, ...)`, where `q` is either `pykx.q` or an instance of `pykx.QConnection`, and `t` was obtained from `q`.
- The context interface now works over IPC.
- Nulls and infinities are now handled as nulls and infinities, rather than as their underlying values. `pykx.Atom.is_null`, `pykx.Atom.is_inf`, `pykx.Collection.has_nulls`, and `pykx.Collection.has_infs` have been added. Numpy, Pandas, and PyArrow handles integral nulls with masked arrays, and they handle temporal nulls with `NaT`. `NaN` continues to be used for real/float nulls. The general Python representation (from `.py()`) uses `K` objects for nulls and infinities.
- Calling `bool` on `pykx.K` objects now either raises a `TypeError`, or return the unambiguously correct result. For ambiguous cases such as `pykx.Collection` instances, use `.any()`, `.all()`, or a length check instead.
- Assignment to q reserved words or the q context now raises a `pykx.PyKXException`.
- `pykx.toq.from_list` (previously `pykdb.adapt.adapt_list`) now works in unlicensed mode.
- `q.query` and `q.sql` are now placeholders (set to `None`). The query interface can be accessed from `q.qsql`.
- Ternary `pow` now raises `TypeError` for `RealNumericVector` and `RealNumericAtom`.
- `QContext` objects are now context handlers, e.g. `with pykx.q.dbmaint: # operate in .dbmaint within this block`. This context handler supports arbitrary nesting.
- `__getitem__` now raises a `pykx.LicenseException` when used in unlicensed mode. Previously it worked for a few select types only. If running in unlicensed mode, one should perform all q indexing in the connected q process, and all Python indexing after converting the `K` object to a Python/Numpy/Pandas/PyArrow object.
- `pykx.QConnection` (previously `pykdb.ipc.Connection`) objects now have an informative/idiomatic repr.
- Calls to `pykx.q` now support up to 8 arguments beyond the required query at position 0, similar to calling `pykx.QConnection` instances. These arguments are applied to the result of the query.
- Embedded q is now used to count the number of rows a table has.
- All dynamic linking to `libq` and `libe` has been replaced by dynamic loading. As a result, the modules previously known as `adapt` and `adapt_unlicensed` have been unified under `pykx.toq`.
- PyKX now attempts to initialize embedded q when `pykx` is imported, rather than when `pykx.q` is first accessed. As a result, the error-prone practice of supplying the `pykx.kdb` singleton class with arguments for embedded q is now impossible.
- Arguments for embedded q can now be supplied via the environment variable `$QARGS` in the form of command-line arguments. For example, `QARGS='--unlicensed'` causes PyKX to enter unlicensed mode when it is started, and `QARGS='-o 8'` causes embedded q to use an offset from UTC of 8 hours. These could be combined as `QARGS='--unlicensed -o 8'`.
- Added the `--licensed` startup flag (to be provided via the `$QARGS` environment variable), which can be used to raise a `pykx.PyKXException` (rather than emitting a warning) if PyKX fails to start in licensed mode (likely because of a missing/invalid q license).
- PyKX Linux wheels are now [PEP 600](https://peps.python.org/pep-0600/) compliant, built to the `manylinux_2_17` standard.
- Misc other bug fixes.
- Misc doc improvements.

### Performance Improvements

- Converting nested lists from q to Python is much faster.
- Internally, PyKX now calls q functions with arguments directly instead of creating a `pykx.Function` instance then calling it. This results in modest performance benefits in some cases.
- The context interface no longer loads every element of a context when the context is first accessed, thereby removing the computation spike, which could be particularly intense for large q contexts.

### New Alpha Features

!!! danger "Alpha features are subject to change"

    Alpha features are not stable will be subject to changes without notice. Use at your own risk.

- q can now load PyKX by loading the q file `pykx.q`. `pykx.q` can be copied into `$QHOME` by running `pykx.install_into_QHOME()`. When loaded into q, it will define the `.pykx` namespace, which notably has `.pykx.exec` and `.pykx.pyeval`. This allows for Python code to be run within q libraries and applications without some of the limitations of embedded q such as the lack of the q main loop, or the lack of timers. When q loads `pykx.q`, it attempts to source the currently active Python environment by running `python`, then fetching the environment details from it.
