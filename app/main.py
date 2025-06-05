from nicegui import ui, app
from typing import Dict, Any
import asyncio
import httpx
import plotly.graph_objects as go
from datetime import datetime
import random

# Add custom CSS for modern styling
ui.add_head_html('''
<style>
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #e2e8f0;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .demo-container {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .success-message {
        background: #10b981;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #ef4444;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
''')

# Global state for demo data
demo_state = {
    'counter': 0,
    'user_name': '',
    'selected_theme': 'blue',
    'chart_data': [],
    'api_status': 'Ready',
    'notifications': []
}


@ui.page('/')
async def index():
    """Main showcase page with interactive components"""
    
    # Hero Section
    with ui.card().classes('hero-section w-full'):
        ui.label('🚀 NiceGUI Interactive Showcase').classes('text-4xl font-bold mb-4')
        ui.label('Explore modern Python web applications with real-time interactivity').classes('text-xl opacity-90')
        
        with ui.row().classes('mt-6 gap-4'):
            ui.button('Get Started', on_click=lambda: ui.notify('Welcome to the showcase!', type='positive')).props('color=white text-color=primary size=lg')
            ui.button('View Features', on_click=lambda: ui.navigate.to('/features')).props('color=white text-color=primary outline size=lg')

    # Quick Stats Dashboard
    with ui.row().classes('w-full gap-4 mb-6'):
        with ui.card().classes('stat-card flex-1'):
            ui.label('1,234').classes('metric-value')
            ui.label('Active Users').classes('metric-label')
        
        with ui.card().classes('stat-card flex-1'):
            ui.label('98.5%').classes('metric-value')
            ui.label('Uptime').classes('metric-label')
        
        with ui.card().classes('stat-card flex-1'):
            ui.label('42ms').classes('metric-value')
            ui.label('Response Time').classes('metric-label')
        
        with ui.card().classes('stat-card flex-1'):
            ui.label('5.0★').classes('metric-value')
            ui.label('User Rating').classes('metric-label')

    # Interactive Demo Section
    with ui.card().classes('demo-container w-full'):
        ui.label('🎮 Interactive Components Demo').classes('text-2xl font-bold mb-4')
        
        with ui.row().classes('w-full gap-6'):
            # Left Column - Controls
            with ui.column().classes('flex-1'):
                ui.label('User Controls').classes('text-lg font-semibold mb-3')
                
                name_input = ui.input('Your Name', value=demo_state['user_name']).classes('w-full')
                name_input.on('input', lambda e: update_user_name(e.value))
                
                ui.separator()
                
                ui.label('Counter Demo').classes('text-md font-semibold mt-4 mb-2')
                counter_display = ui.label(f'Count: {demo_state["counter"]}').classes('text-xl font-bold text-blue-600')
                
                with ui.row().classes('gap-2'):
                    ui.button('➕', on_click=lambda: increment_counter(counter_display)).props('color=positive')
                    ui.button('➖', on_click=lambda: decrement_counter(counter_display)).props('color=negative')
                    ui.button('🔄', on_click=lambda: reset_counter(counter_display)).props('color=warning')
                
                ui.separator()
                
                ui.label('Theme Selector').classes('text-md font-semibold mt-4 mb-2')
                theme_select = ui.select(['blue', 'green', 'purple', 'orange'], value=demo_state['selected_theme'])
                theme_select.on('update:model-value', lambda e: update_theme(e.value))
            
            # Right Column - Live Chart
            with ui.column().classes('flex-1'):
                ui.label('📊 Live Data Visualization').classes('text-lg font-semibold mb-3')
                chart_container = ui.html().classes('w-full h-64')
                
                ui.button('📈 Generate New Data', on_click=lambda: update_chart(chart_container)).props('color=primary')
                
                # Initialize chart
                await update_chart(chart_container)

    # Feature Grid
    ui.label('✨ Key Features').classes('text-2xl font-bold mt-8 mb-4')
    
    with ui.grid(columns=3).classes('w-full gap-4'):
        # Real-time Updates
        with ui.card().classes('feature-card'):
            ui.label('⚡').classes('text-4xl mb-2')
            ui.label('Real-time Updates').classes('text-lg font-semibold mb-2')
            ui.label('Live data synchronization and instant UI updates without page refreshes.').classes('text-gray-600')
        
        # Modern UI Components
        with ui.card().classes('feature-card'):
            ui.label('🎨').classes('text-4xl mb-2')
            ui.label('Modern UI Components').classes('text-lg font-semibold mb-2')
            ui.label('Beautiful, responsive components with smooth animations and interactions.').classes('text-gray-600')
        
        # Python Native
        with ui.card().classes('feature-card'):
            ui.label('🐍').classes('text-4xl mb-2')
            ui.label('Python Native').classes('text-lg font-semibold mb-2')
            ui.label('Build full-stack applications using only Python - no JavaScript required.').classes('text-gray-600')
        
        # Easy Deployment
        with ui.card().classes('feature-card'):
            ui.label('🚀').classes('text-4xl mb-2')
            ui.label('Easy Deployment').classes('text-lg font-semibold mb-2')
            ui.label('Deploy to cloud platforms with minimal configuration and setup.').classes('text-gray-600')
        
        # Data Integration
        with ui.card().classes('feature-card'):
            ui.label('📊').classes('text-4xl mb-2')
            ui.label('Data Integration').classes('text-lg font-semibold mb-2')
            ui.label('Seamless integration with databases, APIs, and data processing libraries.').classes('text-gray-600')
        
        # Responsive Design
        with ui.card().classes('feature-card'):
            ui.label('📱').classes('text-4xl mb-2')
            ui.label('Responsive Design').classes('text-lg font-semibold mb-2')
            ui.label('Mobile-first design that works perfectly on all devices and screen sizes.').classes('text-gray-600')


@ui.page('/features')
async def features_page():
    """Detailed features demonstration page"""
    
    with ui.card().classes('w-full p-6'):
        ui.button('← Back to Home', on_click=lambda: ui.navigate.to('/')).props('flat color=primary')
        
        ui.label('🔧 Advanced Features Demo').classes('text-3xl font-bold mt-4 mb-6')
        
        # API Integration Demo
        with ui.card().classes('w-full p-4 mb-6'):
            ui.label('🌐 API Integration Demo').classes('text-xl font-semibold mb-4')
            
            api_status = ui.label(f'Status: {demo_state["api_status"]}').classes('text-lg')
            api_result = ui.html().classes('mt-4')
            
            async def test_api():
                api_status.text = 'Status: Loading...'
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get('https://httpbin.org/json', timeout=5.0)
                        data = response.json()
                        api_status.text = 'Status: ✅ Success'
                        api_result.content = f'''
                        <div class="success-message">
                            <strong>API Response:</strong><br>
                            <pre>{str(data)[:200]}...</pre>
                        </div>
                        '''
                except Exception as e:
                    api_status.text = 'Status: ❌ Error'
                    api_result.content = f'''
                    <div class="error-message">
                        <strong>Error:</strong> {str(e)}
                    </div>
                    '''
            
            ui.button('🔄 Test API Call', on_click=test_api).props('color=primary')
        
        # Form Validation Demo
        with ui.card().classes('w-full p-4 mb-6'):
            ui.label('📝 Form Validation Demo').classes('text-xl font-semibold mb-4')
            
            email_input = ui.input('Email Address').classes('w-full')
            password_input = ui.input('Password', password=True).classes('w-full')
            validation_result = ui.html()
            
            def validate_form():
                email = email_input.value
                password = password_input.value
                
                errors = []
                if not email or '@' not in email:
                    errors.append('Valid email required')
                if not password or len(password) < 6:
                    errors.append('Password must be at least 6 characters')
                
                if errors:
                    validation_result.content = f'''
                    <div class="error-message">
                        <strong>Validation Errors:</strong><br>
                        {'<br>'.join(errors)}
                    </div>
                    '''
                else:
                    validation_result.content = '''
                    <div class="success-message">
                        <strong>✅ Form is valid!</strong>
                    </div>
                    '''
            
            ui.button('Validate Form', on_click=validate_form).props('color=primary')
        
        # File Upload Demo
        with ui.card().classes('w-full p-4'):
            ui.label('📁 File Upload Demo').classes('text-xl font-semibold mb-4')
            
            upload_result = ui.html()
            
            def handle_upload(e):
                upload_result.content = f'''
                <div class="success-message">
                    <strong>File uploaded:</strong> {e.name}<br>
                    <strong>Size:</strong> {len(e.content)} bytes<br>
                    <strong>Type:</strong> {e.type}
                </div>
                '''
            
            ui.upload(on_upload=handle_upload, max_file_size=1_000_000).props('accept=".txt,.json,.csv"')


@ui.page('/health')
async def health_check():
    """Health check endpoint for monitoring"""
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}


# Helper functions for interactivity
def update_user_name(name: str):
    demo_state['user_name'] = name
    if name:
        ui.notify(f'Hello, {name}! 👋', type='positive')


def increment_counter(display):
    demo_state['counter'] += 1
    display.text = f'Count: {demo_state["counter"]}'


def decrement_counter(display):
    demo_state['counter'] -= 1
    display.text = f'Count: {demo_state["counter"]}'


def reset_counter(display):
    demo_state['counter'] = 0
    display.text = f'Count: {demo_state["counter"]}'
    ui.notify('Counter reset! 🔄', type='info')


def update_theme(theme: str):
    demo_state['selected_theme'] = theme
    ui.notify(f'Theme changed to {theme}! 🎨', type='positive')


async def update_chart(container):
    """Generate and update the live chart"""
    # Generate sample data
    x_data = list(range(10))
    y_data = [random.randint(10, 100) for _ in range(10)]
    
    # Create Plotly chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines+markers',
        name='Sample Data',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Live Data Chart',
        xaxis_title='Time',
        yaxis_title='Value',
        height=250,
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Update the chart container
    container.content = fig.to_html(include_plotlyjs='cdn', div_id='chart')
    
    ui.notify('Chart updated! 📊', type='positive')


# Error handling for the application
@app.exception_handler(404)
async def not_found(request, exc):
    with ui.card().classes('w-full max-w-md mx-auto mt-20 p-6 text-center'):
        ui.label('404 - Page Not Found').classes('text-2xl font-bold mb-4')
        ui.label('The page you are looking for does not exist.').classes('text-gray-600 mb-4')
        ui.button('Go Home', on_click=lambda: ui.navigate.to('/')).props('color=primary')


@app.exception_handler(500)
async def server_error(request, exc):
    with ui.card().classes('w-full max-w-md mx-auto mt-20 p-6 text-center'):
        ui.label('500 - Server Error').classes('text-2xl font-bold mb-4')
        ui.label('Something went wrong on our end.').classes('text-gray-600 mb-4')
        ui.button('Go Home', on_click=lambda: ui.navigate.to('/')).props('color=primary')