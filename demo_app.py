"""Demo application for cjm-fasthtml-interactions library.

This demo showcases:

1. StepFlow Pattern:
   - Multi-step wizard workflow
   - State management across steps
   - Progress indicator with daisyUI steps component
   - Form data collection and submission
   - Back/forward/cancel navigation
   - Workflow resumability

2. AsyncLoadingContainer Pattern:
   - Asynchronous content loading with loading indicators
   - Multiple loading styles (spinner, dots, ring, ball, etc.)
   - Customizable loading messages
   - Support for skeleton loaders
"""

from fasthtml.common import *
from cjm_fasthtml_daisyui.core.resources import get_daisyui_headers
from cjm_fasthtml_daisyui.core.testing import create_theme_persistence_script
from cjm_fasthtml_app_core.components.navbar import create_navbar
from cjm_fasthtml_app_core.core.routing import register_routes

# Import demo routers
from demo.step_flow_demo import step_flow_ar, registration_router
from demo.async_loading_demo import async_loading_ar
from demo.home import home_ar

print("\n" + "="*70)
print("Initializing cjm-fasthtml-interactions Demo")
print("="*70)

# Create the FastHTML app
APP_ID = "interact"

app, rt = fast_app(
    pico=False,
    hdrs=[
        *get_daisyui_headers(),
        create_theme_persistence_script(),
    ],
    title="FastHTML Interactions Demo",
    htmlkw={'data-theme': 'light'},
    session_cookie=f'session_{APP_ID}_',
    secret_key=f'{APP_ID}-demo-secret',
)

print("✓ FastHTML app created successfully")

# Create navbar with all routes
print("✓ Creating navbar...")
navbar = create_navbar(
    title="Interactions Demo",
    nav_items=[
        ("Home", home_ar.index),
        ("StepFlow", step_flow_ar.index),
        ("Async Loading", async_loading_ar.index),
    ],
    home_route=home_ar.index,
    theme_selector=True
)

print("  ✓ Navbar created")

# Register all routes
print("✓ Registering routes...")
register_routes(
    app,
    home_ar,
    step_flow_ar,
    registration_router,
    async_loading_ar,
)

# Debug: Print all registered routes
print("\n" + "="*70)
print("Registered Routes:")
print("="*70)
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"  {route.path} -> {route.name if hasattr(route, 'name') else 'unknown'}")

print("\n" + "="*70)
print("Demo App Ready!")
print("="*70)
print("\n📦 Library Components:")
print("  • StepFlow - Multi-step wizard pattern")
print("  • AsyncLoadingContainer - Async content loading with loaders")
print("  • InteractionContext - Unified context management")
print("  • InteractionHtmlIds - Centralized ID constants")
print("  • Step - Declarative step definition")
print("  • LoadingType - Enum for loading indicator styles")
print("="*70 + "\n")


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading

    def open_browser(url):
        print(f"🌐 Opening browser at {url}")
        webbrowser.open(url)

    port = 5021
    host = "0.0.0.0"
    display_host = 'localhost' if host in ['0.0.0.0', '127.0.0.1'] else host

    print(f"🚀 Server: http://{display_host}:{port}")
    print("\n📍 Available routes:")
    print(f"  http://{display_host}:{port}/                    - Homepage")
    print(f"  http://{display_host}:{port}/step_flow/          - StepFlow demo (Registration)")
    print(f"  http://{display_host}:{port}/async_loading/      - AsyncLoadingContainer demo")
    print("\n" + "="*70 + "\n")

    # Open browser after a short delay
    timer = threading.Timer(1.5, lambda: open_browser(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    # Start server
    uvicorn.run(app, host=host, port=port)
