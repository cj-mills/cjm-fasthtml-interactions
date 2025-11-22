"""Demo application for cjm-fasthtml-interactions library.

This demo showcases:

1. StepFlow Pattern:
   - Multi-step wizard workflow
   - State management across steps
   - Progress indicator with daisyUI steps component
   - Form data collection and submission
   - Back/forward/cancel navigation
   - Workflow resumability

2. TabbedInterface Pattern:
   - Tab-based navigation with DaisyUI styling
   - Automatic route generation
   - On-demand content loading
   - Direct URL navigation support
   - Multiple tab styles (lift, bordered, boxed)

3. MasterDetail Pattern:
   - Sidebar navigation with master list
   - Detail content area
   - Hierarchical grouping with collapsible sections
   - Badge indicators for status/counts
   - Active state management with URL synchronization
   - On-demand content loading

4. AsyncLoadingContainer Pattern:
   - Asynchronous content loading with loading indicators
   - Multiple loading styles (spinner, dots, ring, ball, etc.)
   - Customizable loading messages
   - Support for skeleton loaders

5. ModalDialog Pattern:
   - Modal dialogs with DaisyUI styling
   - Multiple size presets
   - Auto-show support
   - HTMX integration for dynamic content

6. SSEConnectionMonitor Pattern:
   - Server-Sent Events connection monitoring
   - Visual status indicators (Live, Disconnected, Error, Reconnecting)
   - Automatic reconnection with exponential backoff
   - Tab visibility awareness
   - Server shutdown detection

7. Pagination Pattern:
   - Automatic route generation and state management
   - Pagination math handled automatically
   - Query parameter preservation
   - Flexible data loading and rendering
   - HTMX integration for SPA-like navigation
"""

from fasthtml.common import *
from cjm_fasthtml_daisyui.core.resources import get_daisyui_headers
from cjm_fasthtml_daisyui.core.testing import create_theme_persistence_script
from cjm_fasthtml_sse.helpers import insert_htmx_sse_ext
from cjm_fasthtml_app_core.components.navbar import create_navbar
from cjm_fasthtml_app_core.core.routing import register_routes

# Import demo routers
from demo.step_flow_demo import step_flow_ar, registration_router
from demo.tabbed_interface_demo import tabbed_interface_ar, dashboard_router
from demo.master_detail_demo import master_detail_ar, browser_router
from demo.async_loading_demo import async_loading_ar
from demo.modal_dialog_demo import modal_dialog_ar
from demo.sse_monitor_demo import sse_monitor_ar
from demo.pagination_demo import pagination_ar, example1_router, example2_router, example3_router, example4_router
from demo.home import home_ar

print("\n" + "="*70)
print("Initializing cjm-fasthtml-interactions Demo")
print("="*70)

# Create the FastHTML app
app, rt = fast_app(
    pico=False,
    hdrs=[
        *get_daisyui_headers(),
        create_theme_persistence_script(),
    ],
    title="FastHTML Interactions Demo",
    htmlkw={'data-theme': 'light'}
)

# Add HTMX SSE extension for Server-Sent Events support
insert_htmx_sse_ext(app.hdrs)

print("✓ FastHTML app created successfully")

# Create navbar with all routes
print("✓ Creating navbar...")
navbar = create_navbar(
    title="Interactions Demo",
    nav_items=[
        ("Home", home_ar.index),
        ("StepFlow", step_flow_ar.index),
        ("Tabbed UI", tabbed_interface_ar.index),
        ("Master-Detail", master_detail_ar.index),
        ("Async Loading", async_loading_ar.index),
        ("Modal Dialog", modal_dialog_ar.index),
        ("SSE Monitor", sse_monitor_ar.index),
        ("Pagination", pagination_ar.index)
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
    tabbed_interface_ar,
    dashboard_router,
    master_detail_ar,
    browser_router,
    async_loading_ar,
    modal_dialog_ar,
    sse_monitor_ar,
    pagination_ar,
    example1_router,
    example2_router,
    example3_router,
    example4_router
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
print("  • TabbedInterface - Tab-based navigation pattern")
print("  • MasterDetail - Sidebar navigation pattern")
print("  • AsyncLoadingContainer - Async content loading with loaders")
print("  • ModalDialog - Modal dialog pattern with DaisyUI styling")
print("  • SSEConnectionMonitor - SSE connection monitoring with status indicators")
print("  • InteractionContext - Unified context management")
print("  • InteractionHtmlIds - Centralized ID constants")
print("  • Step - Declarative step definition")
print("  • Tab - Declarative tab definition")
print("  • DetailItem - Declarative detail item definition")
print("  • DetailItemGroup - Declarative detail group definition")
print("  • LoadingType - Enum for loading indicator styles")
print("  • ModalSize - Enum for modal size presets")
print("  • PaginationStyle - Enum for pagination display styles")
print("  • SSEConnectionConfig - Configuration for SSE monitoring")
print("  • Pagination - Automatic route generation for paginated content")
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
    print(f"  http://{display_host}:{port}/tabbed_interface/   - TabbedInterface demo (Dashboard)")
    print(f"  http://{display_host}:{port}/master_detail/      - MasterDetail demo (File Browser)")
    print(f"  http://{display_host}:{port}/async_loading/      - AsyncLoadingContainer demo")
    print(f"  http://{display_host}:{port}/modal_dialogs/      - ModalDialog demo")
    print(f"  http://{display_host}:{port}/sse_monitor/        - SSEConnectionMonitor demo")
    print(f"  http://{display_host}:{port}/pagination_demo/    - Pagination demo")
    print("\n" + "="*70 + "\n")

    # Open browser after a short delay
    timer = threading.Timer(1.5, lambda: open_browser(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    # Start server
    uvicorn.run(app, host=host, port=port)
