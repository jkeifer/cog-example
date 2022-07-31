# Cog examples

Cog is a simple little tool with dramatic potential, allowing the use of python
as a file preprocessor. One key area of use is document preprocessing, allowing
code execution for dynamic document generation.

This repo aims to be a working example of such a use of cog. The format targeted
here is simply markdown documents viewable in rendered format via GitHub, but
the ideas presented here could certainly be extended to other formats.


## More info on cog

The purpose here is not to document cog. For more information, please see
[the author's page about the tool](https://nedbatchelder.com/code/cog).

One critical note is that for the cog code to be omitted from a rendered/compiled
document, it must be enclosed with a comment block (or each line commented
in language/formats lacking block comments). This is because cog _is not a
templating engine_, it is a preprocessor.

Unless, of course, you want the cog code in the final output, which is the case
for some of the examples herein. Just something to keep in mind.


## Dynamic table of contents

We can easily use python to list files in a directory, placing links here.
But first, we need to learn some things about cog:

```
[[[cog
import cog
try:
    cog.outl(__file__)
except Exception as e:
    cog.outl(str(e))
]]]
name '__file__' is not defined
[[[end]]] (checksum: a6a558141c3f5cd72bc735d9ee53dd82)
```

So it appears `__file__` is not defined, and we can't build paths from it.
Have no fear though, cog helps us here, providing an `inFile` attribute;
we'll use that next.

We also see that we have to call `str` on the exception object, as it seems
`cog.outl` does not resolve non-string objects to a string representation
via a `__repr__` method.

Lastly, the checksums are an addition by cog to ensure no manual changes have
been made to the cog output between executions. If the existing output checksum
does not match the stated on, it will raise an error so the issue can be
reconcilled. 

Anyway, on to the `inFile` attribute:

```
[[[cog
from pathlib import Path
this_file = Path(cog.inFile).resolve()
cog.outl(str(this_file))
]]]
/Users/jkeifer/cog-example/README.md
[[[end]]] (checksum: 42b80144b5a514c30eb08564a9227167)
```

`inFile` indeed allows us to reference the input file, as promised.

Also important to note: imports are preserved between cog code blocks within
the same file. That is, we didn't have to re-import cog in this block. Notice
how this feature makes it possible to have an output-less cog block at the top
of a file with all required imports for those that follow, in the typical
pythonic fashion?

Similarly, all names are retained between cog blocks. We can take advantage of
that fact and reuse `this_file` as we finally get to an example of a dynamic table
of contents:

```
[[[cog
cog.outl('```')  # this is to end our example code block before the output
cog.outl('### Table of contents')
this_dir = this_file.parent
docs_dir = this_dir.joinpath('docs')
for doc in docs_dir.iterdir():
    if doc.suffix == '.md':
        link_name = " ".join(doc.stem.split("_")).capitalize()
        cog.outl(f'* [{link_name}](./{doc.name})')
cog.outl('```')  # create a new code block for the end
]]]
```
### Table of contents
* [Calling shell commands](./calling_shell_commands.md)
* [Cog as a pre-commit hook](./cog_as_a_pre-commit_hook.md)
```
[[[end]]] (checksum: 2d525f1a6c118c300dd64b74f9fbfd31)
```

## Running cog

Now that we have some cog-able docs, we need to find them and cog them.
In our case, we know we are sticking to `.md` files, so it is easy to do
something like the following:

```
$ find . -name '*.md' -exec cog -rc {} +
```

The options provided to cog here are as follows:

* `-r`: run cog in place against each input file, overwriting them with the generated output
* `-c`: use output checksums to protect manual changes from being clobbered unintentionally
