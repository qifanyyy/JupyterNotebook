import taskflow.config as cfg
import visdom
import numpy as np
import traceback

# CAUTION ############
# Hacky solution
# will probabily not work anywhere else

__config__ = cfg.load_config()


def get_server():
    return __config__['backend']['sftp']['host']


class VisdomLogger:

    def __init__(self, host=None, env='main'):

        if host is None:
            self.host = get_server()
        else:
            self.host = host

        self.viz = visdom.Visdom(
            server=self.host
        )
        self.env = env
        self.plots = {}

    def _plot(self, var_name, split_name, title_name, x, y):
        try:
            if var_name not in self.plots:
                self.plots[var_name] = self.viz.line(X=np.array([x,x]), Y=np.array([y,y]), env=self.env, opts=dict(
                    legend=[split_name],
                    title=title_name,
                    xlabel='steps',
                    ylabel=var_name
                ))
            else:
                self.viz.line(X=np.array([x]), Y=np.array([y]), env=self.env,
                              win=self.plots[var_name],
                              name=split_name, update='append')
        except Exception:
            traceback.print_exc()

    def log_loss(self, name, it, train_loss, val_loss=None):
        self._plot(name+'_loss', 'train', 'Rank Loss', it, train_loss)
        if val_loss is not None:
            self._plot(name+'_loss', 'val', 'Rank Loss', it, val_loss)

    def log_acc(self, name, epoch, val_score):
        self._plot(name+'_acc', 'val', 'Spearmann Score', epoch, val_score)
