hashify
=======

**Hard linkink is required.**

Create a tree of destination files based on the cryptographically hashed 
contents of a source tree of files.

This is meant to be a very fuzzy solution wherein like files are potentially 
grouped together into a directory.

The purpose of this project is to seed information useful to ``rsync`` using the 
``--fuzzy`` flag.

Atomicity is not required for this to do a best effort job.  This solution works 
well without filesystem snapshots and works precisely with filesystem snapshots.

Why?
----

Rsync has a difficult time noticing when files move or are renamed.  Rsync does 
however support fuzzy searching which can offer a huge bonus when a file is 
renamed within a certain Levenshtein distance (typically 25 according to rsync 
source code).

For instance if side a has ``filename.txt`` and side b has ``filename.TXT`` the 
similarities of the files size as well as the files name together help support 
fuzzy matching and each file is compared via a series of block checksums to 
efficiently create a matched transfer.

If filename.txt were moved on side a to a completely different directory this is 
now lost.

Creating a directory where the contents of ``filename.txt`` which we assume is 
identical to that of ``filename.TXT`` on side b is hashed and used as the 
directory name we can then place a hard link to ``filename.txt`` into that 
directory.

The sneaky bit is that the name ``filename.txt`` itself is hashed as well.  The 
shortest possible non existing string in that hash is used to store the link.  
This helps assure that the Levenshtein distance requirement is within range.

This program can optionally clean up the directory used for storing the links by 
iterating through each link file and removing any links that have a hard link 
reference count (st_ino) of 1.  1 means they are isolated and the file in the 
source directory was most likely deleted.

Usage
-----

This program has very low error handling.  As well it shouldn't.  You are 
warned.

You will need an initial sum directory for optimal operation.

``hashify --logging=debug --cleanup --batch=10 --hash=md5sum /dir/to/files/ /dir/to/..files.sums/``

Doing this will use ``/dir/to/files/`` as the source and relative paths within 
that path are summed and new directories are created under ``/dir/to/..files.sums/``.

The output directory contains a double dot which helps it be sorted in first for 
processing by rsync which is very important.

Sync both to a remote server somewhere

``rsync --fuzzy --numeric-ids --delete --relative --stats -i -avPHS /dir/to/..files.sums/ /dir/to/files/ user@somewhere:/dir/for/mirror/``

The ``-H`` or ``--hard-links`` flag is the important bit that will make sure 
rsync stores a list of inodes for later use when processing the source 
directory used to create the sums.

Now you are ready to change filees around in ``/dir/to/files/`` by moving large 
trees of information around as a test.

The next step can be optimized by first running rsync in dry run mode and making 
a list of the files, using ``-i`` or ``--itemize-changes`` and feeding that 
directly to ``hashify``.

Rerun ``hashify`` (optionally with changes file list only)

Rerun ``rsync`` (do not use the changes file)

There should be quite a bit of information returned via the ``--stats`` flag.  
One of which being ``Matched Transfer`` which should be substantially higher 
than ``Actual Transfer``.

Gotchas
-------

The scope of the transfer is very important.  In order to retain hard links you 
must iterate over all files that could possibly contain the reference link in 
order to allow the remote side to properly create a mapping based on the inode 
references available to it.  They will not be the same.

Todo
----

Test creating a set of 1024k sums of the head of each file and use that as well 
and test with ``--append-verify`` on top of ``--fuzzy``
