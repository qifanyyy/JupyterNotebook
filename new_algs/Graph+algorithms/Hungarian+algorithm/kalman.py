import numpy as np

class Kalman():
    def init(self, dt, u, std_acc, std_pos, X_init=np.zeros((4,1)), P_init=np.eye(4)):
        self.dt = dt
        self.u = np.ones((2, 1)) * u
        self.x = X_init
        self.A = np.array([[1, 0, self.dt, 0],
                           [0, 1, 0, self.dt],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
        self.B = np.array([[(self.dt ** 2) / 2, 0],
                           [(self.dt ** 2) / 2, 0],
                           [self.dt, 0],
                           [0, self.dt]])
        self.H = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0]])
        self.Q = np.array([[(self.dt ** 4) / 4, 0, (self.dt ** 3) / 2, 0],
                           [0, (self.dt ** 4) / 4, 0, (self.dt ** 3) / 2],
                           [(self.dt ** 3) / 2, 0, self.dt ** 2, 0],
                           [0, (self.dt ** 3) / 2, 0, self.dt ** 2]]) * std_acc ** 2
        self.R = np.eye(2) * std_pos ** 2
        self.P = P_init

    def predict(self):
        self.x = np.dot(self.A, self.x) + np.dot(self.B, self.u)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x

    def correct(self, z):
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x = np.round(self.x + np.dot(K, (z - np.dot(self.H, self.x))))
        I = np.eye(self.H.shape[1])
        self.P = (I - np.dot(np.dot(K, self.H), self.P))
        return self.x
