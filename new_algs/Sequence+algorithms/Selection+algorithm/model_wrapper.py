import numpy as np
import pandas as pd
import sklearn


class SklearnModelWrapper:

    def __init__(self, model, single):
        self.model_template = model
        self.model = None
        self.single = single
        self.columns = None

    def fit(self, train_dataframe):
        if self.single:
            self.model, self.columns = self._fit_single_model(train_dataframe, self.model_template)
        else:
            self.model, self.columns = self._fit_multi_model(train_dataframe, self.model_template)

    def predict(self, test_dataframe):
        if self.single:
            return self._predict_single_model(test_dataframe, self.model, self.columns)
        else:
            return self._predict_multi_model(test_dataframe, self.model, self.columns)

    @staticmethod
    def _frame_to_X_and_y(frame, original_columns):
        y = frame['objective_function']
        frame = frame.drop(['instance_id', 'objective_function'], axis=1)

        if original_columns is not None:
            missing_cols = set(original_columns) - set(frame)
            additional_cols = set(frame) - set(original_columns)
            for missing in missing_cols:
                frame.loc[:, missing] = 0

            for additional in additional_cols:
                del frame[additional]
            frame = frame[original_columns]

        return frame.as_matrix(), y.as_matrix(), frame.columns.values

    @staticmethod
    def _fit_multi_model(train_dataframe, pipeline):
        algorithms = train_dataframe.algorithm.unique()
        models = dict()

        expected_size = int(len(train_dataframe) / len(algorithms))

        columns = None
        for algorithm_id in algorithms:
            train_algorithm = train_dataframe.loc[train_dataframe['algorithm'] == algorithm_id]
            if len(train_algorithm) != expected_size:
                raise ValueError('Train frame wrong size. Excepted %d got %d' % (expected_size, len(train_algorithm)))
            train_X, train_y, curr_columns = SklearnModelWrapper._frame_to_X_and_y(
                pd.get_dummies(train_algorithm.drop(['algorithm'], axis=1), columns=['step_1']), None)
            if columns is None:
                columns = curr_columns
            else:
                if not np.array_equal(columns, curr_columns):
                    raise ValueError()
            pipeline_algorithm = sklearn.base.clone(pipeline)
            pipeline_algorithm.fit(train_X, train_y)
            models[algorithm_id] = pipeline_algorithm
        return models, columns

    @staticmethod
    def _predict_multi_model(test_dataframe, models, original_columns):
        algorithms = test_dataframe.algorithm.unique()
        test_task_ids = test_dataframe.instance_id.unique()

        task_algorithm_pred = {task: dict() for task in test_task_ids}

        for task_id in test_task_ids:
            test_frame = test_dataframe[test_dataframe['instance_id'] == task_id]

            for algorithm_id in algorithms:
                test_algorithm = test_frame.loc[test_frame['algorithm'] == algorithm_id]
                if len(test_algorithm) != 1:
                    raise ValueError()
                test_X, _, _ = SklearnModelWrapper._frame_to_X_and_y(pd.get_dummies(test_algorithm.drop(['algorithm'], axis=1), columns=['step_1']), original_columns)
                y_hat = models[algorithm_id].predict(test_X)

                task_algorithm_pred[task_id][algorithm_id] = y_hat[0]
        return task_algorithm_pred

    @staticmethod
    def _fit_single_model(train_dataframe, pipeline):
        model = sklearn.base.clone(pipeline)
        train_X, train_y, columns = SklearnModelWrapper._frame_to_X_and_y(pd.get_dummies(train_dataframe, columns=['algorithm', 'step_1']), None)
        model.fit(train_X, train_y)
        return model, columns

    @staticmethod
    def _predict_single_model(test_dataframe, model, original_columns):
        algorithms = test_dataframe.algorithm.unique()
        test_task_ids = test_dataframe.instance_id.unique()

        task_algorithm_pred = {task: dict() for task in test_task_ids}

        for task_id in test_task_ids:
            test_frame = pd.get_dummies(test_dataframe[test_dataframe['instance_id'] == task_id], columns=['algorithm', 'step_1'])

            for algorithm_id in algorithms:
                test_algorithm = test_frame.loc[test_frame['algorithm_' + str(algorithm_id)] == 1]
                if len(test_algorithm) != 1:
                    raise ValueError()
                test_X, _, _ = SklearnModelWrapper._frame_to_X_and_y(test_algorithm, original_columns)
                y_hat = model.predict(test_X)

                task_algorithm_pred[task_id][algorithm_id] = y_hat[0]
        return task_algorithm_pred
