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
"""

from pathlib import Path
from fasthtml.common import *
from cjm_fasthtml_daisyui.core.resources import get_daisyui_headers
from cjm_fasthtml_daisyui.core.testing import create_theme_persistence_script

print("\n" + "="*70)
print("Initializing cjm-fasthtml-interactions Demo")
print("="*70)

# Import library components
from cjm_fasthtml_interactions.patterns.step_flow import Step, StepFlow
from cjm_fasthtml_interactions.patterns.tabbed_interface import Tab, TabbedInterface
from cjm_fasthtml_interactions.core.context import InteractionContext
from cjm_fasthtml_interactions.core.html_ids import InteractionHtmlIds
from cjm_fasthtml_app_core.core.html_ids import AppHtmlIds
from cjm_fasthtml_app_core.core.htmx import handle_htmx_request
from cjm_fasthtml_app_core.core.layout import wrap_with_layout
from cjm_fasthtml_app_core.components.navbar import create_navbar

# Import utilities for styling
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.sizing import container, max_w, w
from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight, text_align
from cjm_fasthtml_tailwind.utilities.flexbox_and_grid import grid_display, grid_cols, gap
from cjm_fasthtml_tailwind.core.base import combine_classes
from cjm_fasthtml_daisyui.components.actions.button import btn, btn_colors, btn_sizes
from cjm_fasthtml_daisyui.components.data_display.card import card, card_body, card_title
from cjm_fasthtml_daisyui.components.data_input.text_input import text_input
from cjm_fasthtml_daisyui.components.data_input.select import select
from cjm_fasthtml_daisyui.components.navigation.link import link, link_colors

print("✓ All library components imported successfully")

# Create the FastHTML app at module level
app, rt = fast_app(
    pico=False,
    hdrs=[
        *get_daisyui_headers(),
        create_theme_persistence_script(),
    ],
    title="FastHTML Interactions Demo",
    htmlkw={'data-theme': 'light'}
)

# Define step render functions for registration workflow
def render_name_step(ctx: InteractionContext):
    """Render step 1 - collect name."""
    current_name = ctx.get("name", "")
    return Div(
        H2("Enter Your Name", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        Label("Full Name:", cls=combine_classes(font_weight.semibold, m.b(2))),
        Input(
            name="name",
            value=current_name,
            placeholder="John Doe",
            required=True,
            cls=combine_classes(text_input, 'input-bordered', w.full)
        ),
        cls=combine_classes(card_body)
    )

def render_email_step(ctx: InteractionContext):
    """Render step 2 - collect email."""
    name = ctx.get("name", "there")
    current_email = ctx.get("email", "")
    return Div(
        H2(f"Hi {name}! What's your email?",
           cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        Label("Email Address:", cls=combine_classes(font_weight.semibold, m.b(2))),
        Input(
            name="email",
            type="email",
            value=current_email,
            placeholder="john@example.com",
            required=True,
            cls=combine_classes(text_input, 'input-bordered', w.full)
        ),
        cls=combine_classes(card_body)
    )

def render_preferences_step(ctx: InteractionContext):
    """Render step 3 - collect preferences."""
    current_notifications = ctx.get("notifications", "")
    return Div(
        H2("Set Your Preferences",
           cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        Label("Notification Preferences:", cls=combine_classes(font_weight.semibold, m.b(2))),
        Select(
            Option("Daily updates", value="daily", selected=(current_notifications == "daily")),
            Option("Weekly digest", value="weekly", selected=(current_notifications == "weekly")),
            Option("Monthly summary", value="monthly", selected=(current_notifications == "monthly")),
            name="notifications",
            cls=combine_classes(select, 'select-bordered', w.full)
        ),
        cls=combine_classes(card_body)
    )

def render_confirm_step(ctx: InteractionContext):
    """Render step 4 - confirmation."""
    name = ctx.get("name", "")
    email = ctx.get("email", "")
    notifications = ctx.get("notifications", "")
    return Div(
        H2("Confirm Your Information",
           cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        Div(
            P(Strong("Name: "), name, cls=str(m.b(2))),
            P(Strong("Email: "), email, cls=str(m.b(2))),
            P(Strong("Notifications: "), notifications.title(), cls=str(m.b(4))),
            P("Click 'Complete Registration' to finish.",
              cls=combine_classes(text_align.center, m.t(4))),
            cls=combine_classes(p(4))
        ),
        cls=combine_classes(card_body)
    )

# Define completion handler
def on_registration_complete(state: dict, request):
    """Handle registration completion."""
    name = state.get("name", "")
    email = state.get("email", "")
    return Div(
        Div(
            H2("Registration Complete! 🎉",
               cls=combine_classes(font_size._3xl, font_weight.bold, m.b(4), text_align.center)),
            P(f"Welcome, {name}!",
              cls=combine_classes(font_size.xl, m.b(2), text_align.center)),
            P(f"We've sent a confirmation email to {email}",
              cls=combine_classes(text_align.center, m.b(6))),
            Div(
                A(
                    "Start Another Registration",
                    href=registration_router.start.to(),
                    hx_get=registration_router.start.to(),
                    hx_target=f"#{InteractionHtmlIds.STEP_FLOW_CONTAINER}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.primary)
                ),
                cls=combine_classes(text_align.center)
            ),
            cls=combine_classes(card_body)
        ),
        cls=combine_classes(card, max_w.lg, m.x.auto, m.t(8))
    )

# Create registration step flow with progress indicator
registration_flow = StepFlow(
    flow_id="registration",
    steps=[
        Step(
            id="name",
            title="Name",
            render=render_name_step,
            data_keys=["name"]
        ),
        Step(
            id="email",
            title="Email",
            render=render_email_step,
            data_keys=["email"]
        ),
        Step(
            id="preferences",
            title="Preferences",
            render=render_preferences_step,
            data_keys=["notifications"]
        ),
        Step(
            id="confirm",
            title="Confirm",
            render=render_confirm_step,
            next_button_text="Complete Registration"
        )
    ],
    on_complete=on_registration_complete,
    show_progress=True  # Enable progress indicator
)

# Generate router and register it
registration_router = registration_flow.create_router(prefix="/register")
registration_router.to_app(app)

# ========================================
# Tabbed Interface Demo
# ========================================

# Define tab render functions for dashboard
def render_overview_tab(ctx: InteractionContext):
    """Render overview tab."""
    stats = ctx.get_data("stats", {})
    return Div(
        H2("Dashboard Overview", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        P("This tab shows a dashboard overview with statistics.",
          cls=combine_classes(m.b(6))),
        Div(
            Div(
                H3("Total Items", cls=combine_classes(font_weight.semibold, m.b(2))),
                P(str(stats.get("total", 0)), cls=combine_classes(font_size._3xl, font_weight.bold)),
                cls=combine_classes(card_body)
            ),
            Div(
                H3("Active Items", cls=combine_classes(font_weight.semibold, m.b(2))),
                P(str(stats.get("active", 0)), cls=combine_classes(font_size._3xl, font_weight.bold)),
                cls=combine_classes(card_body)
            ),
            cls=combine_classes(grid_display, grid_cols._1, grid_cols._2.md, gap._4)
        ),
        cls=combine_classes(card_body)
    )

def render_settings_tab(ctx: InteractionContext):
    """Render settings tab."""
    return Div(
        H2("Settings", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        P("Configure your application preferences here.",
          cls=combine_classes(m.b(4))),
        Div(
            Label("Theme:", cls=combine_classes(font_weight.semibold, m.b(2))),
            Select(
                Option("Light", value="light"),
                Option("Dark", value="dark"),
                Option("Cupcake", value="cupcake"),
                cls=combine_classes(select, 'select-bordered', w.full, max_w.xs)
            ),
            cls=str(m.b(4))
        ),
        Div(
            Label("Language:", cls=combine_classes(font_weight.semibold, m.b(2))),
            Select(
                Option("English", value="en"),
                Option("Spanish", value="es"),
                Option("French", value="fr"),
                cls=combine_classes(select, 'select-bordered', w.full, max_w.xs)
            ),
            cls=str(m.b(4))
        ),
        cls=combine_classes(card_body)
    )

def render_help_tab(ctx: InteractionContext):
    """Render help tab."""
    return Div(
        H2("Help & Documentation", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        P("Find helpful resources and documentation here.",
          cls=combine_classes(m.b(4))),
        Div(
            H3("Quick Links", cls=combine_classes(font_weight.semibold, m.b(3))),
            Ul(
                Li(A("Getting Started Guide", href="#", cls=combine_classes(link, link_colors.primary))),
                Li(A("API Reference", href="#", cls=combine_classes(link, link_colors.primary))),
                Li(A("Common Issues", href="#", cls=combine_classes(link, link_colors.primary))),
                Li(A("Contact Support", href="#", cls=combine_classes(link, link_colors.primary))),
                cls=combine_classes(m.l(6))
            )
        ),
        cls=combine_classes(card_body)
    )

def render_about_tab(ctx: InteractionContext):
    """Render about tab."""
    return Div(
        H2("About", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        P("This demo showcases the TabbedInterface pattern from cjm-fasthtml-interactions.",
          cls=combine_classes(m.b(4))),
        Div(
            H3("Features", cls=combine_classes(font_weight.semibold, m.b(3))),
            Ul(
                Li("DaisyUI radio-based tab navigation"),
                Li("Automatic route generation"),
                Li("On-demand content loading"),
                Li("Direct URL navigation support"),
                Li("Multiple tab styles (lift, bordered, boxed)"),
                cls=combine_classes(m.l(6), m.b(4))
            )
        ),
        Div(
            H3("Version", cls=combine_classes(font_weight.semibold, m.b(2))),
            P("cjm-fasthtml-interactions v0.1.0", cls=str(m.b(4)))
        ),
        cls=combine_classes(card_body)
    )

# Optional data loader for overview tab
def load_dashboard_stats(request):
    """Load statistics for overview tab."""
    return {
        "stats": {
            "total": 156,
            "active": 42
        }
    }

# Create tabbed interface with lift style
dashboard_tabs = TabbedInterface(
    interface_id="dashboard",
    tabs_list=[
        Tab(
            id="overview",
            label="Overview",
            title="Dashboard Overview",
            render=render_overview_tab,
            data_loader=load_dashboard_stats
        ),
        Tab(
            id="settings",
            label="Settings",
            title="Configuration Settings",
            render=render_settings_tab
        ),
        Tab(
            id="help",
            label="Help",
            title="Help & Documentation",
            render=render_help_tab
        ),
        Tab(
            id="about",
            label="About",
            title="About This Demo",
            render=render_about_tab
        )
    ],
    tab_style="lift"  # Use DaisyUI lift style
)

# Generate router and register it
dashboard_router = dashboard_tabs.create_router(prefix="/dashboard")
dashboard_router.to_app(app)

# Define main routes at module level
@rt
def index(request):
    """Homepage with library overview."""

    def home_content():
        return Div(
            H1("cjm-fasthtml-interactions Demo",
               cls=combine_classes(font_size._4xl, font_weight.bold, m.b(4))),

            P("Reusable user interaction patterns for FastHTML applications:",
              cls=combine_classes(font_size.lg, m.b(6))),

            # Feature list
            Div(
                Div(
                    H3("StepFlow Pattern", cls=combine_classes(font_weight.bold, m.b(2))),
                    Ul(
                        Li("Multi-step wizard workflows"),
                        Li("Visual progress indicators"),
                        Li("Form data collection"),
                        Li("State management and resumability"),
                        cls=combine_classes(m.l(6), m.b(4))
                    )
                ),
                Div(
                    H3("TabbedInterface Pattern", cls=combine_classes(font_weight.bold, m.b(2))),
                    Ul(
                        Li("DaisyUI radio-based tabs"),
                        Li("Automatic route generation"),
                        Li("On-demand content loading"),
                        Li("Multiple tab styles"),
                        cls=combine_classes(m.l(6), m.b(8))
                    )
                ),
                cls=combine_classes(text_align.left, m.b(8))
            ),

            # Navigation
            Div(
                A(
                    "StepFlow Demo",
                    href=registration_router.start.to(),
                    cls=combine_classes(btn, btn_colors.primary, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "Tabbed Interface Demo",
                    href=dashboard_router.index.to(),
                    cls=combine_classes(btn, btn_colors.secondary, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "View Features",
                    href=features.to(),
                    hx_get=features.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.accent, btn_sizes.lg, m.b(2))
                ),
            ),

            cls=combine_classes(
                container,
                max_w._4xl,
                m.x.auto,
                p(8),
                text_align.center
            )
        )

    return handle_htmx_request(
        request,
        home_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
    )

@rt
def features(request):
    """Page listing all library features."""

    def features_content():
        return Div(
            H1("StepFlow Pattern Features",
               cls=combine_classes(font_size._3xl, font_weight.bold, m.b(6))),

            # StepFlow Pattern
            Div(
                H2("StepFlow Class", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
                P("Multi-step wizard pattern with automatic route generation:",
                  cls=combine_classes(m.b(2))),
                Ul(
                    Li("Define steps declaratively with ", Code("Step"), " objects"),
                    Li("Automatic route generation (start, next, back, reset)"),
                    Li("State persistence with ", Code("WorkflowSession")),
                    Li("Optional progress indicator with daisyUI steps"),
                    Li("Form data collection and validation"),
                    Li("Customizable navigation buttons"),
                    cls=combine_classes(m.l(6), m.b(6))
                ),
            ),

            # Context Management
            Div(
                H2("InteractionContext", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
                P("Unified context for step rendering:",
                  cls=combine_classes(m.b(2))),
                Ul(
                    Li("Access to workflow state (", Code("ctx.get()"), ", ", Code("ctx.set()"), ")"),
                    Li("Custom data from loaders (", Code("ctx.get_data()"), ")"),
                    Li("Request and session objects"),
                    Li("Batch state updates (", Code("ctx.update_state()"), ")"),
                    cls=combine_classes(m.l(6), m.b(6))
                ),
            ),

            # Navigation
            Div(
                H2("Navigation Controls", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
                P("Built-in navigation with proper HTMX integration:",
                  cls=combine_classes(m.b(2))),
                Ul(
                    Li("Back button (returns to previous step)"),
                    Li("Continue/Submit button (advances or completes)"),
                    Li("Cancel button (resets workflow)"),
                    Li("Form-aware (proper button types for submission)"),
                    cls=combine_classes(m.l(6), m.b(6))
                ),
            ),

            # HTML IDs
            Div(
                H2("InteractionHtmlIds", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
                P("Centralized HTML ID constants:",
                  cls=combine_classes(m.b(2))),
                Ul(
                    Li(f"STEP_FLOW_CONTAINER = '{InteractionHtmlIds.STEP_FLOW_CONTAINER}'"),
                    Li(f"STEP_FLOW_PROGRESS = '{InteractionHtmlIds.STEP_FLOW_PROGRESS}'"),
                    Li(f"STEP_FLOW_NAVIGATION = '{InteractionHtmlIds.STEP_FLOW_NAVIGATION}'"),
                    Li("Dynamic step IDs via ", Code("step_content()"), " and ", Code("step_indicator()")),
                    cls=combine_classes(m.l(6), m.b(6))
                ),
            ),

            cls=combine_classes(
                container,
                max_w._4xl,
                m.x.auto,
                p(8)
            )
        )

    return handle_htmx_request(
        request,
        features_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
    )

# Create navbar at module level (after route definitions so it can reference them)
navbar = create_navbar(
    title="Interactions Demo",
    nav_items=[
        ("Home", index),
        ("StepFlow", registration_router.start),
        ("Tabbed UI", dashboard_router.index),
        ("Features", features)
    ],
    home_route=index,
    theme_selector=True
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
print("  • InteractionContext - Unified context management")
print("  • InteractionHtmlIds - Centralized ID constants")
print("  • Step - Declarative step definition")
print("  • Tab - Declarative tab definition")
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
    print(f"  http://{display_host}:{port}/                  - Homepage")
    print(f"  http://{display_host}:{port}/register/start    - StepFlow demo (Registration)")
    print(f"  http://{display_host}:{port}/dashboard/        - TabbedInterface demo (Dashboard)")
    print(f"  http://{display_host}:{port}/features          - Feature list")
    print("\n" + "="*70 + "\n")

    # Open browser after a short delay
    timer = threading.Timer(1.5, lambda: open_browser(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    # Start server
    uvicorn.run(app, host=host, port=port)
