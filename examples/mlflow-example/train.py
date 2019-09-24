"""
A sample code of MLflow
"""

import numpy as np
import xgboost as xgb
from argparse import ArgumentParser
from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from urllib.request import urlretrieve

import mlflow
import mlflow.sklearn

print('MLflow version:%s' % mlflow.version.VERSION)
print('Tracking URI:%s' % mlflow.tracking.get_tracking_uri())

if __name__ == "__main__":
    # Parses command-line arguments
    parser = ArgumentParser()
    parser.add_argument('--experiment_name', dest='experiment_name', help='Expriment Name', type=str, required=False, default='Default')
    parser.add_argument('--run_name', dest='run_name', help='Run Name', type=str, required=False, default='N/A')
    parser.add_argument('--max_depth', dest='max_depth', help='XGBoost Max Depth', type=str, required=True)
    parser.add_argument('--learning_rate', dest='learning_rate', help='XGBoost Learning Rate', type=str, required=True)
    parser.add_argument('--subsample', dest='subsample', help='XGBoost Subsampling Ratio', type=str, required=True)
    args = parser.parse_args()

    # Set the name for this training
    print('experiment_name:%s' % args.experiment_name)
    mlflow.set_experiment(args.experiment_name)

    # Load iris dataset
    iris = load_iris()

    # Splits `iris` into two parts: training (`X_train` and `y_train`) and
    # test data (`X_test` and `y_test`)
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75)

    # Starts runs with different XGBoost parameters
    for md in args.max_depth.split(','):
        for lr in args.learning_rate.split(','):
            for ssr in args.subsample.split(','):
                # Creates an execution context for a single run with given parameters (`md`, `lr`, and `ssr`)
                with mlflow.start_run(run_name=args.run_name) as run:
                    clf = xgb.XGBClassifier(max_depth=int(md), learning_rate=float(lr), nthread=-1, subsample=float(ssr))
                    clf.fit(X_train, y_train)

                    # Computes a metric for the built model
                    pred = clf.predict(X_test)
                    rmse = np.sqrt(mean_squared_error(y_test, pred))

                    # For better tracking, stores the training logs (the three parameters and the metric)
                    # and the built model in the MLflow logging framework
                    # TODO: Saves a graphviz image for feature importances in XGBoost
                    mlflow.set_tag('training algorithm', 'xgboost')
                    mlflow.log_param('max_depth', md)
                    mlflow.log_param('learning_rate', lr)
                    mlflow.log_param('subsample', ssr)
                    mlflow.log_metric('RMSE', rmse)
                    # TODO: Save the XGBoost model:
                    # https://www.mlflow.org/docs/latest/models.html#example-saving-an-xgboost-model-in-mlflow-format
                    # mlflow.sklearn.log_model(clf, 'model')

                    print('XGBoost model (max_depth=%s, learning_rate=%s, subsample=%s):' % (md, lr, ssr))
                    print('  RMSE: %f' % rmse)
