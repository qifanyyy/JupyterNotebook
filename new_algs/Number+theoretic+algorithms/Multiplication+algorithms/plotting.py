import numpy as np
import numpy.random as npr
import numpy.linalg as la
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)


def plot_trajectories(nr,ell,t_hist,x_hist):
    n = x_hist.shape[-1]
    # Plot the rollout state data
    if ell < 1200 and nr < 4000:
        fig, ax = plt.subplots(n)
        plot_alpha = np.min([1, 10 / nr])
        if n > 1:
            for i in range(n):
                ax[i].step(t_hist, x_hist[:, :, i], color='tab:blue', linewidth=0.5, alpha=plot_alpha)
                ax[i].set_ylabel("State %d" % (i+1))
            ax[-1].set_xlabel("Time step")
            ax[0].set_title("Rollout data")
        else:
            ax.step(t_hist, x_hist[:, :, 0], color='tab:blue', linewidth=0.5, alpha=plot_alpha)
            ax.set_ylabel("State")
            ax.set_xlabel("Time step")
            ax.set_title("Rollout data")
    else:
        fig, ax = None, None
    return fig, ax


def plot_model_estimates(A, B, SigmaA, SigmaB, Ahat, Bhat, SigmaAhat, SigmaBhat, split=False, fs=16):
    def minmax(X1, X2):
        return np.min([X1.min(), X2.min()]), np.max([X1.max(), X2.max()])

    def imshow_compare(X1, X2, ax1, ax2, ax3, cmap=None):
        if cmap is None:
            cmap = 'inferno_r'
        vmin, vmax = minmax(X1, X2)
        im1 = ax1.imshow(X1, vmin=vmin, vmax=vmax, cmap=cmap)
        im2 = ax2.imshow(X2, vmin=vmin, vmax=vmax, cmap=cmap)
        im3 = ax3.imshow(np.abs(X1-X2), vmin=0, vmax=np.max(np.abs(X1-X2)), cmap=cmap)
        for i, im, ax in zip([1, 2, 3], [im1, im2, im3], [ax1, ax2, ax3]):
            if i==3:
                cmin, cmax = 0, np.max(np.abs(X1-X2))
            else:
                cmin, cmax = vmin, vmax
            cbar = plt.colorbar(im, ax=ax, ticks=np.linspace(cmin, cmax, 3))
            cbar.ax.tick_params(labelsize=16)
            ax.tick_params(axis='both', which='major', labelsize=16)
            ax.tick_params(axis='both', which='minor', labelsize=16)
        return vmin, vmax, im1, im2, im3

    if A.size + B.size > 2:
        # View the model estimates as matrices
        data = [[X, Xhat] for X, Xhat in zip([A, B, SigmaA, SigmaB], [Ahat, Bhat, SigmaAhat, SigmaBhat])]

        if split:
            figs = []
            axs = []
            idxs_list = [[0, 1], [2, 3]]
            labels_list = [["$A$", "$B$"], ["$\Sigma_A$", "$\Sigma_B$"]]
            for idxs, labels in zip(idxs_list, labels_list):
                fig, ax = plt.subplots(3, 2)
                fig.set_size_inches(6, 6)
                imshow_compare(data[idxs[0]][0], data[idxs[0]][1], ax[0, 0], ax[1, 0], ax[2, 0])
                imshow_compare(data[idxs[1]][0], data[idxs[1]][1], ax[0, 1], ax[1, 1], ax[2, 1])
                ax[0, 0].set_ylabel("True", fontsize=fs)
                ax[1, 0].set_ylabel("Estimate", fontsize=fs)
                ax[2, 0].set_ylabel("Absolute Error", fontsize=fs)
                ax[2, 0].set_xlabel(labels[0], fontsize=int(fs*1.5))
                ax[2, 1].set_xlabel(labels[1], fontsize=int(fs*1.5))


                fig.tight_layout()
                figs.append(fig)
                axs.append(ax)
        else:
            fig, ax = plt.subplots(3, 4)
            fig.set_size_inches(10, 6)

            for i in range(4):
                imshow_compare(data[i][0], data[i][1], ax[0, i], ax[1, i], ax[2, i])

            ax[0, 0].set_ylabel("True", fontsize=fs)
            ax[1, 0].set_ylabel("Estimate", fontsize=fs)
            ax[2, 0].set_ylabel("Absolute Error", fontsize=fs)
            ax[2, 0].set_xlabel("$A$", fontsize=int(fs*1.5))
            ax[2, 1].set_xlabel("$B$", fontsize=int(fs*1.5))
            ax[2, 2].set_xlabel("$\Sigma_A$", fontsize=int(fs*1.5))
            ax[2, 3].set_xlabel("$\Sigma_B$", fontsize=int(fs*1.5))
            fig.tight_layout()
            figs = fig
            axs = ax
    else:
        figs, axs = None, None

    return figs, axs


def plot_estimation_error(tk_hist,Ahat_error_hist,Bhat_error_hist,SigmaAhat_error_hist,SigmaBhat_error_hist,xlabel_str):
    # Plot the model estimation errors
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 6)
    ax.step(tk_hist, Ahat_error_hist, linewidth=2)
    ax.step(tk_hist, Bhat_error_hist, linewidth=2)
    ax.step(tk_hist, SigmaAhat_error_hist, linewidth=2)
    ax.step(tk_hist, SigmaBhat_error_hist, linewidth=2)
    ax.legend(["Ahat", "Bhat", "SigmaAhat", "SigmaBhat"])
    ax.set_xlabel(xlabel_str)
    ax.set_ylabel("Normalized Error")
    # ax.set_yscale("log")
    return fig,ax


def plot_estimation_error_multi(n,m,s_hist,experiment_data,xlabel_str,scale_option='log',show_reference_curve=True):
    # Plot the normalized model estimation errors
    fig,ax = plt.subplots(nrows=2,ncols=2)
    plt.subplots_adjust(wspace=0.4,hspace=0.4)
    fig.set_size_inches(7, 7)
    # title_str_list = ["A", "B", "SigmaA", "SigmaB"]
    title_str_list = ["A", "B", r"$\Sigma_A$", r"$\Sigma_B$"]
    # ylabel_str_list = [r"$ \frac{\|A-\hat{A}\|_F}{\|A\|_F} $",
    #                    r"$ \frac{\|B-\hat{B}\|_F}{\|B\|_F} $",
    #                    r"$ \frac{\|\Sigma_A-\hat{\Sigma}_A \|_F}{\|\Sigma_A\|_F} $",
    #                    r"$ \frac{\|\Sigma_B-\hat{\Sigma}_B \|_F}{\|\Sigma_B\|_F} $"]
    ylabel_str_list = ["Normalized error"]*4
    ax_idx_i = [0,0,1,1]
    ax_idx_j = [0,1,0,1]
    for k in range(4):
        # Get quartiles
        y000 = np.min(experiment_data[k],1)
        y025 = np.percentile(experiment_data[k],25,1)
        y050 = np.percentile(experiment_data[k],50,1)
        y075 = np.percentile(experiment_data[k],75,1)
        y100 = np.max(experiment_data[k],1)
        # Axes indices
        i,j = ax_idx_i[k], ax_idx_j[k]
        # Fill the region between min and max values
        ax[i,j].fill_between(s_hist,y000,y100,step='pre',color=0.6*np.ones(3),alpha=0.5)
        # Fill the interquartile region
        ax[i,j].fill_between(s_hist,y025,y075,step='pre',color=0.3*np.ones(3),alpha=0.5)
        # Plot the individual experiment realizations
        if experiment_data.shape[2] < 8:
            ax[i,j].step(s_hist, experiment_data[k], linewidth=1, alpha=0.6)
        else:
            # ax[i,j].step(s_hist, experiment_data[k], color='tab:blue', linewidth=1, alpha=0.2)
            pass
        # # Plot the mean of the experiments
        # ax[i,j].step(s_hist, np.mean(experiment_data[k],1), color='mediumblue', linewidth=2)
        # Plot the median of the experiments
        median_handle, = ax[i,j].step(s_hist,y050,color='k',linewidth=2)
        # Plot a reference curve for an O(1/sqrt(N)^n or m) convergence rate
        if show_reference_curve:
            ref_scale = 1.5
            exponent = 1 if i==0 else n if j==0 else m
            # exponent = 1
            ref_curve = s_hist**(-0.5/exponent)
            ref_curve *= ref_scale*np.max(np.percentile(experiment_data[k],75,1)/ref_curve)
            ref_handle, = ax[i,j].plot(s_hist, ref_curve, color='r', linewidth=2, linestyle='--')
        if scale_option == 'log':
            ax[i,j].set_xscale("log")
            ax[i,j].set_yscale("log")
        ax[i,j].set_title(title_str_list[k],fontsize=16)
        ax[i,j].set_xlabel(xlabel_str,fontsize=12)
        ax[i,j].set_ylabel(ylabel_str_list[k],rotation=90,fontsize=12)
        # ax[i,j].set_ylim([1e-4,1e1])
        if ax[i,j].get_xscale() is "linear":
            ax[i,j].ticklabel_format(axis='x',style='sci',scilimits=(0,4))
        legend_handles = (median_handle,ref_handle)
        legend_labels = (r"Median",r"$\mathcal{O}\left(n_r^{-1/%d} \right)$" % (2*exponent))
        ax[i,j].legend(legend_handles,legend_labels,fontsize=12)
        xtick_max = np.log10(s_hist.max())
        xtick_vals = np.logspace(0,xtick_max,int(xtick_max)+1)
        ax[i,j].set_xticks(xtick_vals)
        ax[i,j].grid(True,linestyle='--')
    return fig,ax