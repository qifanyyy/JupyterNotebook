#!/usr/bin/env python
# -*- coding: utf-8 -*-


import plotly.offline as py
import plotly.graph_objs as go


def show_plot(times_prim, times_kruskal, edges):
    trace0 = go.Scatter(
        x=edges,
        y=times_prim,
        name='Prim',
        line=dict(
            color=('rgb(205, 12, 24)'),
            width=4)
    )

    trace1 = go.Scatter(
        x=edges,
        y=times_kruskal,
        name='Kruskal',
        line=dict(
            color=('rgb(22, 96, 167)'),
            width=4,)
    )

    data = [trace0, trace1]

    layout = dict(title='Computational Efficiency of Algorithms',
                  xaxis=dict(title='Number of Edges'),
                  yaxis=dict(title='Running Time (s)'))

    fig = dict(data=data, layout=layout)
    py.plot(fig, 'my_plot.png')
