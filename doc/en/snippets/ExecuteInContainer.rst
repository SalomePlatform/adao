.. index:: single: ExecuteInContainer

ExecuteInContainer
  *Optional command*. This variable allows to choose the execution mode in YACS
  in a specific container. In its absence or if its value is "No", no separate
  container is used for execution and it runs in the main YACS process. If its
  value is "Mono", a specific YACS container is created and it is used to host
  the execution of all nodes in the same process. If its value is "Multi", a
  specific YACS container is created and it is used to host the execution of
  each node in a specific process. The default value is "No", and the possible
  choices are "No", "Mono" and "Multi".

  .. warning::

    in its present version, this command is experimental, and therefore remains
    subject to changes in future versions.
