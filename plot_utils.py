import plotly.graph_objects as go

def apply_white_theme(fig):
    """Apply consistent dark theme to plotly figures"""
    fig.update_layout(
        plot_bgcolor='rgba(26, 32, 44, 0.0)',
        paper_bgcolor='rgba(26, 32, 44, 0.0)',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color='#e2e8f0'
        ),
        title=dict(
            font=dict(size=20, color='#e2e8f0'),
            x=0.5,
            xanchor='center'
        ),
        legend=dict(
            bgcolor='rgba(26, 32, 44, 0.3)',
            bordercolor='rgba(99, 179, 237, 0.1)',
            borderwidth=1,
            font=dict(color='#e2e8f0'),
            x=1.02,
            xanchor='left',
            y=1,
            yanchor='auto'
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(99, 179, 237, 0.1)',
            tickfont=dict(size=12, color="#e2e8f0"),
            linecolor='rgba(99, 179, 237, 0.2)',
            linewidth=1,
            ticks='outside'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(99, 179, 237, 0.1)',
            tickfont=dict(size=12, color="#e2e8f0"),
            linecolor='rgba(99, 179, 237, 0.2)',
            linewidth=1,
            ticks='outside'
        )
    )
    return fig
