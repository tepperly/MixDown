#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.59)
AC_INIT([TestCaseB], [1.0], [white238@llnl.gov])
AC_CONFIG_SRCDIR([main.c])
AM_INIT_AUTOMAKE

# Checks for programs.
AC_PROG_CC
AM_PROG_CC_C_O

# Checks for command-line options
AC_ARG_WITH([TestCaseC],
	AS_HELP_STRING([--with-TestCaseC=PATH],
	[Location of TestCaseC]),,)

AC_CONFIG_FILES([Makefile])

AC_OUTPUT
