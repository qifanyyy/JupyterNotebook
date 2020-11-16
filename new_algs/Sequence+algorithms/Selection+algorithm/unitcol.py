
class unitcol:
    def __init__(self):
        pass

    def unitcol_cr(self, IN, W):

        # W = [1 0 1 1 0 1 1 0 1 0];
        # FIGURE 2 | Functional architecture
        # doi: 10.3389 / fnana.2010.00017

        SIN = sum(IN)

        # Dot product
        # U = dot(IN, W)
        U = sum(W)
        V = U / SIN

        print("U ", U)

        return V