# PPDML (Privacy-preserving Distributed Machine Learning)

This repository will show several machine learning in privacy-preserving manner when the data is vertically partitioned. 
The following algorithms have been applied:
* Linear Regression
* Naive Bayes
* Secure multiparty computation

## Privacy-preserving Linear Regression (vertically partitioned data)
_Privacy_preserving_linear_regression.ipynb_ shows how we inmplement the linear regression in a privacy-preserving manner. You can find more details in the notebook. Furthermore, we also dockerized PPLR with using PyTaskManager (https://bitbucket.org/jvsoest/pytaskmanager). Please have a look at the fold <PPLR_Dockerized>

## Data pre-processing before privacy-preserving machine learning
In privacy-preserving machine learning and data minging in a distributed data scenario, we are facing a very challenging problem that the existing solutions are not very feasible and scalable to apply in real-world datasets. The most popular method -secure multiparty computation- takes very high costs of time, communication, and computations. To solve this problem, I suggest we can classify privacy level of features before doing analysis might decrease the cost. More details and code please check _Data pre-processing (privacy-preserving).ipynb_

## [NEW] Privacy-preserving Naive Bayes Classification (vertically partitioned data)
Please go to _Privacy-preserving bayesians_ folder. _Privacy-preserving Naive Bayes (Numercial features).ipynb_ shows how Naive Bayes classification can be done in vertically partitioned data scenairo. We take two situations into account: 1) both parties know the target class; 2) only one party knows the target class. We also applied secure scalar product to calculate mean and variance values.

## [NEW] Privacy-preserving bayesian structure (network) (vertically partitioned data)
Bayesian Network is a probabilistic graphical model (a type of statistical model) that represents a set of variables and their conditional dependencies via a directed acyclic graph (DAG). Here is a very good Structure Model Learning Package: https://github.com/pgmpy/pgmpy In this notebook, so far only K2 algorithm is applied for structure learning. Other algorithms and Parameter Learnings are still working-in-progress.
