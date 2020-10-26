# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Compare how "smooth" plotted values look.

This will contrast three different implementations (``K = 1, 2, 3``)
and show that more accuracy produces smoother plots.
"""

import matplotlib.pyplot as plt
import numpy as np

import de_casteljau
import plot_utils


# p(s) = (s - 1) (s - 3/4)^7
BEZIER_COEFFS = (
    2187.0 / 16384.0,
    -5103.0 / 131072.0,
    729.0 / 65536.0,
    -405.0 / 131072.0,
    27.0 / 32768.0,
    -27.0 / 131072.0,
    3.0 / 65536.0,
    -1.0 / 131072.0,
    0.0,
)
ROOT = 0.75
DELTA_S = 1e-5
NUM_POINTS = 401


def main(filename=None):
    s_vals = np.linspace(ROOT - DELTA_S, ROOT + DELTA_S, NUM_POINTS)

    evaluated1 = []
    evaluated2 = []
    evaluated3 = []

    for s in s_vals:
        b, db, d2b = de_casteljau._compensated_k(s, BEZIER_COEFFS, 3)
        evaluated1.append(b)
        b2 = b + db
        evaluated2.append(b2)
        b3 = b2 + d2b
        evaluated3.append(b3)

    figure, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True)
    ax1.plot(s_vals, evaluated1)
    ax2.plot(s_vals, evaluated2)
    ax3.plot(s_vals, evaluated3)

    # Since ``sharex=True``, ticks only need to be set once.
    ax1.set_xticks(
        [
            ROOT - DELTA_S,
            ROOT - 0.5 * DELTA_S,
            ROOT,
            ROOT + 0.5 * DELTA_S,
            ROOT + DELTA_S,
        ]
    )

    ax1.set_title(r"$\mathtt{DeCasteljau}$")
    ax2.set_title(r"$\mathtt{CompDeCasteljau}$")
    ax3.set_title(r"$\mathtt{CompDeCasteljau3}$")

    if filename is None:
        plt.show()
    else:
        figure.set_size_inches(13.65, 6.41)
        figure.subplots_adjust(
            left=0.04,
            bottom=0.10,
            right=0.97,
            top=0.95,
            wspace=0.15,
            hspace=0.19,
        )
        path = plot_utils.get_path(filename)
        figure.savefig(path, bbox_inches="tight")
        print("Saved {}".format(filename))
        plt.close(figure)


if __name__ == "__main__":
    plot_utils.set_styles()
    main(filename="de_casteljau_smooth_drawing.pdf")
