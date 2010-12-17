AC_DEFUN([CHECK_MODULE_EFICAS],[

AC_CHECKING(for Module Eficas)

module_eficas_ok=no

AC_ARG_WITH(module-eficas,
            [  --with-module-eficas=DIR               root directory path of Module Eficas installation],
               MODULE_EFICAS_DIR=$withval,MODULE_EFICAS_DIR="")

if test "x$MODULE_EFICAS_DIR" = "x" ; then

  # no --with-module-eficas option used

  if test "x$EFICAS_ROOT_DIR" != "x" ; then

  #EFICAS_ROOT_DIR environment variable defined
  MODULE_EFICAS_DIR=$EFICAS_ROOT_DIR

  else
    AC_MSG_WARN("EFICAS_ROOT_DIR is not defined")
  fi
fi

if test "x$MODULE_EFICAS_DIR" != "x" ; then
  module_eficas_ok=yes
fi

AC_MSG_RESULT(for Module Eficas: $module_eficas_ok)

])dnl

