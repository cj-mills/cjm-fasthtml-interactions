"""Demo application for cjm-fasthtml-interactions library.

This demo showcases the StepFlow pattern:
- Multi-step wizard workflow
- State management across steps
- Progress indicator with daisyUI steps component
- Form data collection and submission
- Back/forward/cancel navigation
- Workflow resumability
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
from cjm_fasthtml_interactions.core.context import InteractionContext
from cjm_fasthtml_interactions.core.html_ids import InteractionHtmlIds
from cjm_fasthtml_app_core.core.html_ids import AppHtmlIds
from cjm_fasthtml_app_core.core.htmx import handle_htmx_request
from cjm_fasthtml_app_core.core.layout import wrap_with_layout
from cjm_fasthtml_app_core.components.navbar import create_navbar

print("✓ All library components imported successfully")


def main():
    """Main entry point - creates the demo app."""

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

    # Import utilities for styling
    from cjm_fasthtml_tailwind.utilities.spacing import p, m
    from cjm_fasthtml_tailwind.utilities.sizing import container, max_w
    from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight, text_align
    from cjm_fasthtml_tailwind.core.base import combine_classes
    from cjm_fasthtml_daisyui.components.actions.button import btn, btn_colors, btn_sizes
    from cjm_fasthtml_daisyui.components.data_display.card import card, card_body, card_title

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
                cls="input input-bordered w-full"
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
                cls="input input-bordered w-full"
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
                cls="select select-bordered w-full"
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
                        href="/register",
                        hx_get="/register",
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

    # Define main routes
    @rt("/")
    def home(request):
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
                        Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                        Span("Multi-step wizard workflows with state management"),
                        cls=combine_classes(m.b(3))
                    ),
                    Div(
                        Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                        Span("Visual progress indicators using daisyUI steps"),
                        cls=combine_classes(m.b(3))
                    ),
                    Div(
                        Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                        Span("Form data collection across multiple steps"),
                        cls=combine_classes(m.b(3))
                    ),
                    Div(
                        Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                        Span("Back/forward/cancel navigation controls"),
                        cls=combine_classes(m.b(3))
                    ),
                    Div(
                        Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                        Span("Automatic route generation and resumability"),
                        cls=combine_classes(m.b(8))
                    ),
                    cls=combine_classes(text_align.left, m.b(8))
                ),

                # Navigation (Note: /register routes are handled by registration_router)
                Div(
                    A(
                        "Try Registration Demo",
                        href="/register",
                        cls=combine_classes(btn, btn_colors.primary, btn_sizes.lg, m.r(2))
                    ),
                    A(
                        "View Features",
                        href="/features",
                        hx_get="/features",
                        hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                        hx_push_url="true",
                        cls=combine_classes(btn, btn_colors.secondary, btn_sizes.lg)
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

        # Create navbar
        my_navbar = create_navbar(
            title="Interactions Demo",
            nav_items=[
                ("Home", home),
                ("Features", features)
            ],
            home_route=home,
            theme_selector=True
        )

        return handle_htmx_request(
            request,
            home_content,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=my_navbar)
        )

    @rt("/features")
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

        my_navbar = create_navbar(
            title="Interactions Demo",
            nav_items=[
                ("Home", home),
                ("Features", features)
            ],
            home_route=home,
            theme_selector=True
        )

        return handle_htmx_request(
            request,
            features_content,
            wrap_fn=lambda content: wrap_with_layout(content, navbar=my_navbar)
        )

    print("\n" + "="*70)
    print("Demo App Ready!")
    print("="*70)
    print("\n📦 Library Components:")
    print("  • StepFlow - Multi-step wizard pattern")
    print("  • InteractionContext - Unified context management")
    print("  • InteractionHtmlIds - Centralized ID constants")
    print("  • Step - Declarative step definition")
    print("="*70 + "\n")

    return app


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading

    # Create the app
    app = main()

    def open_browser(url):
        print(f"🌐 Opening browser at {url}")
        webbrowser.open(url)

    port = 5021
    host = "0.0.0.0"
    display_host = 'localhost' if host in ['0.0.0.0', '127.0.0.1'] else host

    print(f"🚀 Server: http://{display_host}:{port}")
    print("\n📍 Available routes:")
    print(f"  http://{display_host}:{port}/              - Homepage")
    print(f"  http://{display_host}:{port}/register      - Registration workflow")
    print(f"  http://{display_host}:{port}/features      - Feature list")
    print("\n" + "="*70 + "\n")

    # Open browser after a short delay
    timer = threading.Timer(1.5, lambda: open_browser(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    # Start server
    uvicorn.run(app, host=host, port=port)
