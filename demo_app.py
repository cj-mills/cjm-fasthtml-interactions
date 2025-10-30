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
from cjm_fasthtml_interactions.patterns.master_detail import MasterDetail, DetailItem, DetailItemGroup
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
from cjm_fasthtml_daisyui.components.data_display.badge import badge_colors
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
            cls=combine_classes(text_input, w.full)
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
            cls=combine_classes(text_input, w.full)
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
            cls=combine_classes(select, w.full)
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

# Generate router and register it
dashboard_router = dashboard_tabs.create_router(prefix="/dashboard")
dashboard_router.to_app(app)

# ========================================
# Master-Detail Demo
# ========================================

# Define detail render functions for file browser
def render_file_detail(ctx: InteractionContext):
    """Render file detail view."""
    file_data = ctx.get_data("file", {})
    return Div(
        H2(f"📄 {file_data.get('name', 'Unknown File')}",
           cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        P("File details and metadata:",
          cls=combine_classes(m.b(4))),
        Div(
            Div(
                H3("File Information", cls=combine_classes(font_weight.semibold, m.b(2))),
                P(Strong("Size: "), f"{file_data.get('size', 0)} bytes", cls=str(m.b(2))),
                P(Strong("Type: "), file_data.get('type', 'N/A'), cls=str(m.b(2))),
                P(Strong("Modified: "), file_data.get('modified', 'N/A'), cls=str(m.b(2))),
                P(Strong("Path: "), file_data.get('path', 'N/A'), cls=str(m.b(4))),
                cls=combine_classes(card_body, m.b(4))
            ),
            Div(
                H3("Actions", cls=combine_classes(font_weight.semibold, m.b(2))),
                Div(
                    Button("Download", cls=combine_classes(btn, btn_colors.primary, btn_sizes.sm, m.r(2))),
                    Button("Share", cls=combine_classes(btn, btn_colors.secondary, btn_sizes.sm, m.r(2))),
                    Button("Delete", cls=combine_classes(btn, btn_colors.error, btn_sizes.sm)),
                ),
                cls=combine_classes(card_body)
            ),
            cls=str(m.t(4))
        ),
        cls=combine_classes(card_body)
    )

def render_folder_detail(ctx: InteractionContext):
    """Render folder detail view."""
    folder_data = ctx.get_data("folder", {})
    return Div(
        H2(f"📁 {folder_data.get('name', 'Unknown Folder')}",
           cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        P("Folder contents and statistics:",
          cls=combine_classes(m.b(4))),
        Div(
            Div(
                H3("Folder Statistics", cls=combine_classes(font_weight.semibold, m.b(2))),
                P(Strong("Total Items: "), str(folder_data.get('item_count', 0)), cls=str(m.b(2))),
                P(Strong("Files: "), str(folder_data.get('file_count', 0)), cls=str(m.b(2))),
                P(Strong("Folders: "), str(folder_data.get('folder_count', 0)), cls=str(m.b(4))),
                cls=combine_classes(card_body, m.b(4))
            ),
            Div(
                H3("Contents", cls=combine_classes(font_weight.semibold, m.b(2))),
                Ul(
                    *[Li(item, cls=str(m.b(1))) for item in folder_data.get('items', [])],
                    cls=combine_classes(m.l(6))
                ),
                cls=combine_classes(card_body)
            ),
            cls=str(m.t(4))
        ),
        cls=combine_classes(card_body)
    )

def render_overview_detail(ctx: InteractionContext):
    """Render storage overview."""
    overview_data = ctx.get_data("overview", {})
    return Div(
        H2("💾 Storage Overview",
           cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        P("Your file storage at a glance:",
          cls=combine_classes(m.b(4))),
        Div(
            Div(
                H3("Storage Summary", cls=combine_classes(font_weight.semibold, m.b(2))),
                P(Strong("Total Files: "), str(overview_data.get('total_files', 0)), cls=str(m.b(2))),
                P(Strong("Total Size: "), overview_data.get('total_size', 'N/A'), cls=str(m.b(2))),
                P(Strong("Available Space: "), overview_data.get('available_space', 'N/A'), cls=str(m.b(4))),
                cls=combine_classes(card_body, m.b(4))
            ),
            Div(
                H3("Quick Stats", cls=combine_classes(font_weight.semibold, m.b(3))),
                Div(
                    Div(
                        P("Documents", cls=combine_classes(font_weight.semibold)),
                        P(str(overview_data.get('documents_count', 0)),
                          cls=combine_classes(font_size._2xl, font_weight.bold)),
                        cls=combine_classes(card_body)
                    ),
                    Div(
                        P("Images", cls=combine_classes(font_weight.semibold)),
                        P(str(overview_data.get('images_count', 0)),
                          cls=combine_classes(font_size._2xl, font_weight.bold)),
                        cls=combine_classes(card_body)
                    ),
                    Div(
                        P("Videos", cls=combine_classes(font_weight.semibold)),
                        P(str(overview_data.get('videos_count', 0)),
                          cls=combine_classes(font_size._2xl, font_weight.bold)),
                        cls=combine_classes(card_body)
                    ),
                    cls=combine_classes(grid_display, grid_cols._1, grid_cols._3.md, gap._4)
                ),
                cls=combine_classes(card_body)
            ),
            cls=str(m.t(4))
        ),
        cls=combine_classes(card_body)
    )

# Data loaders for master-detail items
def load_report_data(request):
    """Load annual report file metadata."""
    return {
        "file": {
            "name": "annual-report.pdf",
            "size": 3145728,  # 3 MB
            "type": "PDF Document",
            "modified": "2025-01-15 09:30",
            "path": "/documents/annual-report.pdf"
        }
    }

def load_presentation_data(request):
    """Load presentation file metadata."""
    return {
        "file": {
            "name": "presentation.pdf",
            "size": 2097152,  # 2 MB
            "type": "PDF Document",
            "modified": "2025-01-20 14:30",
            "path": "/documents/presentation.pdf"
        }
    }

def load_vacation_photo_data(request):
    """Load vacation photo metadata."""
    return {
        "file": {
            "name": "vacation-photo.jpg",
            "size": 524288,  # 512 KB
            "type": "JPEG Image",
            "modified": "2024-12-25 16:45",
            "path": "/media/vacation-photo.jpg"
        }
    }

def load_demo_video_data(request):
    """Load demo video metadata."""
    return {
        "file": {
            "name": "demo-video.mp4",
            "size": 8388608,  # 8 MB
            "type": "MP4 Video",
            "modified": "2025-01-18 11:20",
            "path": "/media/demo-video.mp4"
        }
    }

def load_folder_data(request):
    """Load folder metadata."""
    return {
        "folder": {
            "name": "Work Projects",
            "item_count": 12,
            "file_count": 8,
            "folder_count": 4,
            "items": ["project-plan.docx", "budget.xlsx", "team-photo.jpg", "meeting-notes.txt"]
        }
    }

def load_overview_data(request):
    """Load storage overview data."""
    return {
        "overview": {
            "total_files": 1247,
            "total_size": "8.4 GB",
            "available_space": "41.6 GB",
            "documents_count": 342,
            "images_count": 856,
            "videos_count": 49
        }
    }

# Create master-detail file browser interface
file_browser = MasterDetail(
    interface_id="file_browser",
    master_title="File Browser",
    items=[
        DetailItem(
            id="overview",
            label="Storage Overview",
            render=render_overview_detail,
            data_loader=load_overview_data,
            badge_text="1.2K files",
            badge_color=badge_colors.info
        ),
        DetailItemGroup(
            id="documents",
            title="Documents",
            items=[
                DetailItem(
                    id="doc-report",
                    label="annual-report.pdf",
                    render=render_file_detail,
                    data_loader=load_report_data,
                    badge_text="3 MB",
                    badge_color=badge_colors.info
                ),
                DetailItem(
                    id="doc-presentation",
                    label="presentation.pdf",
                    render=render_file_detail,
                    data_loader=load_presentation_data,
                    badge_text="2 MB",
                    badge_color=badge_colors.info
                ),
                DetailItem(
                    id="folder-work",
                    label="Work Projects",
                    render=render_folder_detail,
                    data_loader=load_folder_data,
                    badge_text="12 items",
                    badge_color=badge_colors.success
                )
            ],
            badge_text="3 items",
            default_open=True
        ),
        DetailItemGroup(
            id="media",
            title="Media Files",
            items=[
                DetailItem(
                    id="img-vacation",
                    label="vacation-photo.jpg",
                    render=render_file_detail,
                    data_loader=load_vacation_photo_data,
                    badge_text="512 KB",
                    badge_color=badge_colors.warning
                ),
                DetailItem(
                    id="video-demo",
                    label="demo-video.mp4",
                    render=render_file_detail,
                    data_loader=load_demo_video_data,
                    badge_text="8 MB",
                    badge_color=badge_colors.error
                )
            ],
            badge_text="2 items",
            default_open=False
        )
    ]
)

# Generate router and register it
browser_router = file_browser.create_router(prefix="/files")
browser_router.to_app(app)

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
                    "Master-Detail Demo",
                    href=browser_router.index.to(),
                    cls=combine_classes(btn, btn_colors.success, btn_sizes.lg, m.r(2), m.b(2))
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
        ("Master-Detail", browser_router.index),
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
print("  • MasterDetail - Sidebar navigation pattern")
print("  • InteractionContext - Unified context management")
print("  • InteractionHtmlIds - Centralized ID constants")
print("  • Step - Declarative step definition")
print("  • Tab - Declarative tab definition")
print("  • DetailItem - Declarative detail item definition")
print("  • DetailItemGroup - Declarative detail group definition")
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
    print(f"  http://{display_host}:{port}/files/            - MasterDetail demo (File Browser)")
    print(f"  http://{display_host}:{port}/features          - Feature list")
    print("\n" + "="*70 + "\n")

    # Open browser after a short delay
    timer = threading.Timer(1.5, lambda: open_browser(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    # Start server
    uvicorn.run(app, host=host, port=port)
