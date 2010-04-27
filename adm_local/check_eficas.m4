AC_DEFUN([CHECK_EFICAS],[

AC_CHECKING(for Eficas)

eficas_ok=no

AC_ARG_WITH(eficas,
	    [  --with-eficas=DIR               root directory path of Eficas installation],
	    EFICAS_DIR=$withval,EFICAS_DIR="")

if test "x$EFICAS_DIR" = "x" ; then

  # no --with-eficas option used

  if test "x$EFICAS_ROOT_DIR" != "x" ; then

  #EFICAS_ROOT_DIR environment variable defined
  EFICAS_DIR=$EFICAS_ROOT_DIR

  else
    AC_MSG_WARN("EFICAS_ROOT_DIR is not defined")
  fi
fi

if test "x$EFICAS_DIR" != "x" ; then
  eficas_ok=yes
  AC_SUBST(EFICAS_DIR)
fi

AC_MSG_RESULT(for Eficas: $eficas_ok)
 
])dnl
 
