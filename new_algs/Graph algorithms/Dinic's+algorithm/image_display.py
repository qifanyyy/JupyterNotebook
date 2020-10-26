""" Display image sequence using matplotlib."""

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


class ImageSequenceRenderer(object):
    """ renders sequence of images provided by ImageSequence """
    def __init__(self, image_sequence):

        # Fix the size of subplot
        self.fig, self.axes = plt.subplots(2, sharey=True, figsize=(10, 5))

        # Set background to be gray
        self.fig.patch.set_facecolor('#333333')

        # Store image sequence in self.seq and display the sequence
        self.seq = image_sequence
        self.image = self.seq.init_image()
        self.image2 = self.seq.init_image_original()

        self.image_figure = plt.subplot2grid((3, 3), (0, 0), colspan=3, rowspan=2)
        self.image_figure.axis('off')
        self.image_plot = self.image_figure.imshow(self.image)
        self.image_figure.set_title('Dinic', color='white')

        self.init_figure = plt.subplot2grid((3, 3), (2, 1))
        self.init_figure.axis('off')
        self.init_plot = plt.imshow(self.image2)
        self.init_figure.set_title('Flow Graph', color = 'white' )

        self.text_figure = plt.subplot2grid((3, 3), (2, 2))
        self.text_figure.axis('off')
        self.text_figure.set_title('',color = 'white')

        plt.subplots_adjust(bottom=0.2)
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, 'Next')
        bnext.on_clicked(self.next)

        plt.show()

    def next(self, event):
        if self.seq.complete():
            self.image_figure.set_title('Completed!')  # TODO better way to show it has completed
            plt.draw()
            return
        self.image, self.image2 = self.seq.next_image()
        if self.image is not None:
            self.image_plot.set_data(self.image)

            self.image_figure.set_title(getattr(self.seq, 'title', "Dinic"))
            self.text_figure.set_title(getattr(self.seq, 'aux_text', ""))

            self.init_plot.set_data(self.image2)
            plt.draw()


class ImageSequence(object):
    """ Class interface to give to ImageSequenceRenderer """
    def __init__(self):
        self.i = 0
        self.count = 0
        self.pics = map(mpimg.imread, ['bw.png', 'hello.jpg'])

    def init_image(self):
        return self.pics[self.i]

    def init_image_original(self):
        return self.pics[self.i]

    def next_image(self):
        self.i = 1 - self.i
        self.count = self.count + 1
        return self.pics[self.i]

    def complete(self):
        return self.count >= 10


def start_gui(imageSequence):
    imageSequenceRenderer = ImageSequenceRenderer(imageSequence)
