MixDown
=======

MixDown is a meta-build tool that makes it easier to build software packages which have multiple dependencies.


Example: building subversion
----------------------------

Here's how you would use MixDown to build subversion.

1. Run the MixDown Importer to create initial MixDown build file for subversion:

    MixDownImporter.py  http://subversion.tigris.org/downloads/subversion-1.6.12.tar.bz2 \
    http://www.eng.lsu.edu/mirrors/apache//apr/apr-1.3.12.tar.bz2 \
    http://www.eng.lsu.edu/mirrors/apache//apr/apr-util-1.3.10.tar.bz2 \
    http://www.webdav.org/neon/neon-0.29.5.tar.gz \
    http://www.sqlite.org/sqlite-autoconf-3070500.tar.gz


2. Run MixDown with the following command to execute the build:

    MixDown.py -v -cb -j4 -ptestPrefix subversion-1.6.12.md


Flags
-----


    -v    verbose
    -j4   have 4 job slots for make
    -cb   clean before (this helps if MixDown fails to build and you want to start from scratch)
    -ptestPrefix  set where MixDown will look for libraries and install everything to


