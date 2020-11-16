import sklearn.linear_model
class sklModel:
    '''
        Comprises of methods which
        are common between the existing
        models.
    ''' 
    def fit(self, x, y):
        '''
            Fits the linear model.
        '''
        self.model = self.model.fit(x, y)
    
    def set_params(self, **params):
        '''
            Set the parameters of this estimator.
        '''
        for param in params:
            if param not in self.valid_params():
                raise ValueError('Invalid parameter: ' + param)
    
    def get_params(self):
        '''
            Get parameters for this estimator.
        '''
        return self.model.get_params()
    
    def predict(self, x):
        '''
            Predict using the linear model
        '''
        return self.model.predict(x)
    
    def score(self, x, y):
        '''
            Returns the coefficient of determination R^2 of the prediction.
        '''
        return self.model.score(x, y)
    
    def valid_params(self):
        '''
            Get a list of valid parameters.
        '''
        return [param for param in self.get_params()]  
