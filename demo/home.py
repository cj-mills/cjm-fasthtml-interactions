"""Homepage and features page for the demo app."""

from demo import *

# Create APIRouter for home routes
home_ar = APIRouter(prefix="")


@home_ar
def index(request):
    """Homepage with library overview."""
    # Import here to avoid circular imports
    from demo.step_flow_demo import step_flow_ar
    from demo.tabbed_interface_demo import tabbed_interface_ar
    from demo.master_detail_demo import master_detail_ar
    from demo.async_loading_demo import async_loading_ar
    from demo.modal_dialog_demo import modal_dialog_ar
    from demo.sse_monitor_demo import sse_monitor_ar
    from demo.pagination_demo import pagination_ar

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
                        cls=combine_classes(m.l(6), m.b(4))
                    )
                ),
                Div(
                    H3("MasterDetail Pattern", cls=combine_classes(font_weight.bold, m.b(2))),
                    Ul(
                        Li("Sidebar navigation with master list"),
                        Li("Hierarchical grouping with collapsible sections"),
                        Li("Badge indicators for status"),
                        Li("Active state management"),
                        cls=combine_classes(m.l(6), m.b(8))
                    )
                ),
                cls=combine_classes(text_align.left, m.b(8))
            ),

            # Navigation
            Div(
                # All patterns now use APIRouter with consistent HTMX navigation
                A(
                    "StepFlow Demo",
                    href=step_flow_ar.index.to(),
                    hx_get=step_flow_ar.index.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.primary, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "Tabbed Interface Demo",
                    href=tabbed_interface_ar.index.to(),
                    hx_get=tabbed_interface_ar.index.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.secondary, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "Master-Detail Demo",
                    href=master_detail_ar.index.to(),
                    hx_get=master_detail_ar.index.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.success, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "Async Loading Demo",
                    href=async_loading_ar.index.to(),
                    hx_get=async_loading_ar.index.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.info, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "Modal Dialog Demo",
                    href=modal_dialog_ar.index.to(),
                    hx_get=modal_dialog_ar.index.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.warning, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "SSE Monitor Demo",
                    href=sse_monitor_ar.index.to(),
                    hx_get=sse_monitor_ar.index.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.error, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "Pagination Demo",
                    href=pagination_ar.index.to(),
                    hx_get=pagination_ar.index.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.success, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "View Features",
                    href=home_ar.features.to(),
                    hx_get=home_ar.features.to(),
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

    # Import navbar from demo_app to avoid circular import
    from demo_app import navbar
    return handle_htmx_request(
        request,
        home_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
    )


@home_ar
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

    # Import navbar from demo_app to avoid circular import
    from demo_app import navbar
    return handle_htmx_request(
        request,
        features_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
    )
