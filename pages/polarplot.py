import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# def feature_plot(features):

#     labels = features.columns.tolist()
#     stats = features.mean().tolist()

#     angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)

#     # close the plot
#     stats = np.concatenate((stats,[stats[0]]))
#     angles = np.concatenate((angles,[angles[0]]))

#     # Size of the figure
#     fig = plt.figure(figsize=(18, 18))

#     ax = fig.add_subplot(221, polar=True)
#     ax.plot(angles, stats, 'o-', linewidth=2, label="Features", color='gray', alpha=0.75)
#     ax.fill(angles, stats, alpha=0.5, facecolor='gray')
#     ax.set_thetagrids(angles[0:7] * 180/np.pi, labels, fontsize=13)

#     ax.set_rlabel_position(250)
#     plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", '0.4', "0.6", "0.8"], color="grey", size=12)
#     plt.ylim(0, 1)

#     plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))

#     st.pyplot(fig, bbox_inches='tight')

def feature_plot(features):
    labels = features.columns.tolist()
    stats = features.mean().tolist()

    df = pd.DataFrame({'labels': labels, 'stats': stats})
    df['angles'] = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

    df = df.append(df.iloc[0], ignore_index=True)

    fig = px.line_polar(df, r='stats', theta='angles', line_close=True)
    fig.update_traces(fill='toself', fillcolor='gray', line=dict(color='gray', width=2))
    fig.update_layout(
        polar=dict(radialaxis=dict(showticklabels=False, ticks='', showline=False),
                    angularaxis=dict(showticklabels=True, linewidth=2, linecolor='grey')),
        showlegend=False,
        height=500
    )

    st.plotly_chart(fig)