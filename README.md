MixDown
=======

MixDown is a meta-build tool that makes it easier to build software packages that have multiple dependencies. It uses a simple input file format to describe package information, and uses a series of heuristics to automatically generate an initial problem input file from a collection of tar, zip files, or download URLs.

MixDown supports the following targets:

 * Local tarballs and zipfiles (e.g., /tmp/foo-1.2.3.tar.gz)
 * Download URLs for tarballs and zipfiles (e.g., http://www.example.com/download/foo-1.2.3.tar.gz)
 * Local directories that contain the source code to be built (e.g., /tmp/foo-1.2.3/)
 * Subversion repositories
 * Mercurial (hg) repositories
 * Git repositories


Examples
--------

Subversion
----------

Here's how you would use MixDown to build subversion. First, create an initial MixDown project file using information from the source tarballs of subversion and its dependencies (the order doesn't matter):

    mixdown --import \
    http://subversion.tigris.org/downloads/subversion-1.6.12.tar.bz2 \
    http://www.eng.lsu.edu/mirrors/apache/apr/apr-1.3.12.tar.bz2 \
    http://www.eng.lsu.edu/mirrors/apache/apr/apr-util-1.3.11.tar.bz2 \
    http://www.webdav.org/neon/neon-0.29.5.tar.gz \
    http://www.sqlite.org/sqlite-autoconf-3070500.tar.gz

This will create a MixDown project file called subversion-1.6.12.md.

Next, execute the build:

    mixdown subversion-1.6.12.md

Usage
-----

MixDown - A tool to simplify building

    Profile Mode: 
        Example Usage: mixdown --profile
    
        Required:
        --profile                 Toggle Profile mode
    
        Optional:
        -d<list>      List of non-recursive search directories (comma-delimited)
           Example: -d/home/foo/bin,/usr/local/bin
        -r            List of recursive search directories (comma-delimited)
           Example: -r/home/foo/bin,/usr/local/bin
        <.mdo output file>   Path to outputted MixDown override group file
    
    Import Mode: 
        Example Usage: mixdown --import foo.tar.gz http://path/to/bar
    
        Required:
        --import                  Toggle Import mode
        <package location list>   Space delimited list of package locations
    
        Optional:
        -i            Interactive Mode
        -v            Verbose Mode
    
    Build Mode (Default): 
        Example Usage: mixdown foo.md
    
        Required:
        <path to .md file>   Path to MixDown project file
    
        Optional:
        -v            Verbose Mode
        -f            Force full rebuild (ignores success of previous build)
        -j<number>    Number of build job slots
        -t<number>    Number of threads used to build concurrent targets
        -s<list>      Add steps to skip for individual targets
           Example: -starget1:preconfig,target2:config
        -o<path>      Specify path to Override Groups file
        -g<Compiler>,<Debug>,<Parallel>  Specify Override Groups
           Example: -gGNU,Debug,MPI
           Example: -gGNU,,
        -p<path>      Override prefix directory
        -b<path>      Override build directory
        -w<path>      Override download directory
        -l<logger>    Override default logger (Console, File, Html)
        -k            Keeps previously existing MixDown directories
    
    Clean Mode: 
        Example Usage: mixdown --clean foo.md
    
        Required:
        --clean              Toggle Clean mode
        <path to .md file>   Path to MixDown project file
    
        Optional:
        -v            Verbose Mode
        -j<number>    Number of build job slots
        -t<number>    Number of threads used to build concurrent targets
        -s<list>      Add steps to skip for individual targets
           Example: -starget1:preconfig,target2:config
        -o<path>      Specify path to Override Groups file
        -g<Compiler>,<Debug>,<Parallel>  Specify Override Groups
           Example: -gGNU,Debug,MPI
           Example: -gGNU,,
        -p<path>      Override prefix directory
        -b<path>      Override build directory
        -w<path>      Override download directory
        -l<logger>    Override default logger (Console, File, Html)
    
    Default Directories:
    Builds:       mdBuild/
    Downloads:    mdDownload/
    Logs:         mdLogFiles/
