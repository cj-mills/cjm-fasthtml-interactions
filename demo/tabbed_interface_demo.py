"""TabbedInterface pattern demo - Dashboard with multiple tabs."""

from fasthtml.common import *
from demo import *

# Create APIRouter for tabbed interface demo
tabbed_interface_ar = APIRouter(prefix="/tabbed_interface")


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
                cls=combine_classes(select, w.full, max_w.xs)
            ),
            cls=str(m.b(4))
        ),
        Div(
            Label("Language:", cls=combine_classes(font_weight.semibold, m.b(2))),
            Select(
                Option("English", value="en"),
                Option("Spanish", value="es"),
                Option("French", value="fr"),
                cls=combine_classes(select, w.full, max_w.xs)
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

# Generate dashboard router
dashboard_router = dashboard_tabs.create_router(prefix="/tabs")


@tabbed_interface_ar
def index(request):
    """TabbedInterface demo index - redirects to dashboard."""
    return RedirectResponse(url=dashboard_router.index.to(), status_code=303)
