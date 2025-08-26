import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_skill_charts(analysis_results):
    """Create skill distribution and comparison charts"""
    matched = len(analysis_results['matched_skills'])
    missing = len(analysis_results['missing_skills'])
    extra = len(analysis_results['extra_skills'])
    
    pie_chart = go.Figure(data=[go.Pie(
        labels=['Matched Skills', 'Missing Skills', 'Extra Skills'],
        values=[matched, missing, extra],
        hole=.3,
        marker_colors=['#26a69a', '#ef5350', '#ffca28'],
        textinfo='label+percent',
        hoverinfo='label+value+percent'
    )])
    pie_chart.update_layout(
        title=dict(text="Skills Distribution", x=0.5, xanchor="center", font=dict(size=16)),
        font=dict(size=12),
        height=350,
        margin=dict(t=50, b=20)
    )
    
    categories = ['Resume Skills', 'JD Skills', 'Matched Skills']
    values = [len(analysis_results['resume_skills']), len(analysis_results['jd_skills']), matched]
    bar_chart = go.Figure([go.Bar(
        x=categories,
        y=values,
        marker_color=['#4a90e2', '#ef5350', '#26a69a'],
        text=values,
        textposition='auto'
    )])
    bar_chart.update_layout(
        title=dict(text="Skills Comparison", x=0.5, xanchor="center", font=dict(size=16)),
        xaxis_title="Category",
        yaxis_title="Number of Skills",
        font=dict(size=12),
        height=350,
        margin=dict(t=50, b=20)
    )
    
    return pie_chart, bar_chart