AC_DEFUN([CHECK_EFICAS],[

AC_CHECKING(for Eficas)

eficas_ok=no

AC_ARG_WITH(eficas,
            [  --with-eficas=DIR               root directory path of Eficas installation],
               EFICAS_DIR=$withval,EFICAS_DIR="")

if test "x$EFICAS_DIR" = "x" ; then

  # no --with-eficas option used

  if test "x$EFICAS_ROOT" != "x" ; then

  #EFICAS_ROOT environment variable defined
  EFICAS_DIR=$EFICAS_ROOT

  else
    AC_MSG_WARN("EFICAS_ROOT is not defined")
  fi
fi

if test "x$EFICAS_DIR" != "x" ; then
  eficas_ok=yes
  AC_SUBST(EFICAS_DIR)
fi

AC_MSG_RESULT(for Eficas: $eficas_ok)

])dnl

