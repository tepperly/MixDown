MixDown
=======

MixDown is a meta-build tool that makes it easier to build software packages that have multiple dependencies. It uses a simple input file format to describe package information, and uses a series of heuristics to automatically generate an initial problem input file from a collection of tar, zip files, or download URLs. 


Example
-------

Here's how you would use MixDown to build subversion. First, create an initial MixDown build file using information from the source tarballs of subversion and its dependencies (the order doesn't matter):

    MixDown --import \
    http://subversion.tigris.org/downloads/subversion-1.6.12.tar.bz2 \
    http://www.eng.lsu.edu/mirrors/apache/apr/apr-1.3.12.tar.bz2 \
    http://www.eng.lsu.edu/mirrors/apache/apr/apr-util-1.3.10.tar.bz2 \
    http://www.webdav.org/neon/neon-0.29.5.tar.gz \
    http://www.sqlite.org/sqlite-autoconf-3070500.tar.gz

This will create a MixDown build file called subversion-1.6.12.md.

Next, execute the build:

    MixDown subversion-1.6.12.md


Usage
-----

    Import Mode: 
        Example Usage: MixDown --import foo.tar.gz http://path/to/bar
    
        Required:
        --import                  Toggle Import mode
        <package location list>   Space delimited list of package locations
    
    Build Mode (Default): 
        Example Usage: MixDown foo.md
    
        Required:
        <path to .md file>   Path to MixDown project file
    
        Optional:
        -p<path>      Override prefix directory
        -b<path>      Override build directory
        -o<path>      Override download directory
        -l<logger>    Override default logger (Console, File, Html)
        -k            Keeps previously existing MixDown directories
    
    Clean Mode: 
        Example Usage: MixDown --clean foo.md
    
        Required:
        --clean              Toggle Clean mode
        <path to .md file>   Path to MixDown project file
    
        Optional:
        -b<path>      Override build directory
        -o<path>      Override download directory
        -l<logger>    Override default logger (Console, File, Html)
    
    Default Directories:
    Builds:       mdBuild/
    Downloads:    mdDownload/
    Logs:         mdLogFiles/

