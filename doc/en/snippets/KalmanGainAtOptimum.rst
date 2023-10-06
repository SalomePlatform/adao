.. index:: single: KalmanGainAtOptimum

KalmanGainAtOptimum
  *List of matrices*. Each element is a standard Kalman gain matrix, evaluated
  using the linearized observation operator. It is calculated at the optimal
  state.

  Example:
  ``kg = ADD.get("KalmanGainAtOptimum")[-1]``
