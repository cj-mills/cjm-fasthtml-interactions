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

7. PaginationControls Pattern:
   - Navigation between pages of content
   - Automatic disabled states for boundary pages
   - HTMX integration for SPA-like navigation
   - Multiple display styles (simple, compact)
   - Customizable button text and styling
"""

from pathlib import Path
from fasthtml.common import *
from cjm_fasthtml_daisyui.core.resources import get_daisyui_headers
from cjm_fasthtml_daisyui.core.testing import create_theme_persistence_script
from cjm_fasthtml_sse.helpers import insert_htmx_sse_ext

print("\n" + "="*70)
print("Initializing cjm-fasthtml-interactions Demo")
print("="*70)

# Import library components
from cjm_fasthtml_interactions.patterns.step_flow import Step, StepFlow
from cjm_fasthtml_interactions.patterns.tabbed_interface import Tab, TabbedInterface
from cjm_fasthtml_interactions.patterns.master_detail import MasterDetail, DetailItem, DetailItemGroup
from cjm_fasthtml_interactions.patterns.async_loading import AsyncLoadingContainer, LoadingType
from cjm_fasthtml_interactions.patterns.modal_dialog import ModalDialog, ModalTriggerButton, ModalSize
from cjm_fasthtml_interactions.patterns.sse_connection_monitor import SSEConnectionMonitor, SSEConnectionConfig
from cjm_fasthtml_interactions.patterns.pagination import PaginationControls, PaginationStyle
from cjm_fasthtml_interactions.core.context import InteractionContext
from cjm_fasthtml_interactions.core.html_ids import InteractionHtmlIds
from cjm_fasthtml_app_core.core.html_ids import AppHtmlIds
from cjm_fasthtml_app_core.core.htmx import handle_htmx_request
from cjm_fasthtml_app_core.core.layout import wrap_with_layout
from cjm_fasthtml_app_core.components.navbar import create_navbar

# Import utilities for styling
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.sizing import container, max_w, w, h
from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight, text_align
from cjm_fasthtml_tailwind.utilities.flexbox_and_grid import grid_display, grid_cols, gap, flex_display, items, justify
from cjm_fasthtml_tailwind.core.base import combine_classes
from cjm_fasthtml_daisyui.components.actions.button import btn, btn_colors, btn_sizes, btn_styles
from cjm_fasthtml_daisyui.components.data_display.card import card, card_body, card_title
from cjm_fasthtml_daisyui.components.data_display.badge import badge_colors
from cjm_fasthtml_daisyui.components.data_input.text_input import text_input
from cjm_fasthtml_daisyui.components.data_input.select import select
from cjm_fasthtml_daisyui.components.navigation.link import link, link_colors
from cjm_fasthtml_daisyui.components.feedback.progress import progress, progress_colors
from cjm_fasthtml_daisyui.utilities.semantic_colors import bg_dui

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

# Add HTMX SSE extension for Server-Sent Events support
insert_htmx_sse_ext(app.hdrs)

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
                    "Async Loading Demo",
                    href=async_loading.to(),
                    hx_get=async_loading.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.info, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "Modal Dialog Demo",
                    href=modal_dialogs.to(),
                    hx_get=modal_dialogs.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.warning, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "SSE Monitor Demo",
                    href=sse_monitor.to(),
                    hx_get=sse_monitor.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.error, btn_sizes.lg, m.r(2), m.b(2))
                ),
                A(
                    "Pagination Demo",
                    href=pagination_demo.to(),
                    hx_get=pagination_demo.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
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
def async_loading(request):
    """Async loading patterns demo page."""
    import time

    def async_content():
        return Div(
            H1("Async Loading Container Pattern",
               cls=combine_classes(font_size._3xl, font_weight.bold, m.b(6), text_align.center)),

            P("The AsyncLoadingContainer pattern enables asynchronous content loading with customizable loading indicators.",
              cls=combine_classes(text_align.center, m.b(8), max_w._3xl, m.x.auto)),

            # Example 1: Spinner loader
            Div(
                H2("Example 1: Spinner Loader",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("Simple spinner with loading message",
                  cls=combine_classes(m.b(4))),
                AsyncLoadingContainer(
                    container_id="spinner-demo",
                    load_url="/async_loading/content/spinner",
                    loading_message="Loading content...",
                    container_cls=str(combine_classes(card, bg_dui.base_100))
                ),
                cls=str(m.b(8))
            ),

            # Example 2: Different loading styles
            Div(
                H2("Example 2: Different Loading Styles",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("Various loading indicator styles from DaisyUI",
                  cls=combine_classes(m.b(4))),
                Div(
                    Div(
                        H3("Dots", cls=combine_classes(font_weight.semibold, m.b(2))),
                        AsyncLoadingContainer(
                            container_id="dots-demo",
                            load_url="/async_loading/content/dots",
                            loading_type=LoadingType.DOTS,
                            loading_size="md",
                            container_cls=str(combine_classes(card, bg_dui.base_100))
                        )
                    ),
                    Div(
                        H3("Ring", cls=combine_classes(font_weight.semibold, m.b(2))),
                        AsyncLoadingContainer(
                            container_id="ring-demo",
                            load_url="/async_loading/content/ring",
                            loading_type=LoadingType.RING,
                            loading_size="md",
                            container_cls=str(combine_classes(card, bg_dui.base_100))
                        )
                    ),
                    Div(
                        H3("Ball", cls=combine_classes(font_weight.semibold, m.b(2))),
                        AsyncLoadingContainer(
                            container_id="ball-demo",
                            load_url="/async_loading/content/ball",
                            loading_type=LoadingType.BALL,
                            loading_size="md",
                            container_cls=str(combine_classes(card, bg_dui.base_100))
                        )
                    ),
                    cls=combine_classes(grid_display, grid_cols._1, grid_cols._3.md, gap._4, m.b(8))
                ),
                cls=str(m.b(8))
            ),

            # Example 3: innerHTML swap
            Div(
                H2("Example 3: Inner Content Swap",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("Container persists, only inner content is swapped",
                  cls=combine_classes(m.b(4))),
                AsyncLoadingContainer(
                    container_id="inner-swap-demo",
                    load_url="/async_loading/content/inner",
                    swap="innerHTML",
                    loading_type=LoadingType.SPINNER,
                    container_cls=str(combine_classes(card, card_body, bg_dui.base_200, p(8)))
                ),
                cls=str(m.b(8))
            ),

            cls=combine_classes(
                container,
                max_w._6xl,
                m.x.auto,
                p(8)
            )
        )

    return handle_htmx_request(
        request,
        async_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
    )

# Async loading content endpoints
@rt("/async_loading/content/spinner")
def async_content_spinner():
    """Return loaded content after delay (spinner example)."""
    import time
    time.sleep(1.5)
    return Div(
        H3("Content Loaded!", cls=combine_classes(font_size.xl, font_weight.bold, m.b(2))),
        P("This content was loaded asynchronously using HTMX after a 1.5 second delay."),
        P(f"Loaded at: {time.strftime('%H:%M:%S')}"),
        id="spinner-demo",
        cls=combine_classes(card, card_body, bg_dui.base_100)
    )

@rt("/async_loading/content/dots")
def async_content_dots():
    """Return loaded content for dots example."""
    import time
    time.sleep(1)
    return Div(
        P("Dots loader", cls=combine_classes(font_weight.semibold, m.b(1))),
        P("Loaded successfully!"),
        id="dots-demo",
        cls=combine_classes(card, card_body, bg_dui.base_100)
    )

@rt("/async_loading/content/ring")
def async_content_ring():
    """Return loaded content for ring example."""
    import time
    time.sleep(1.2)
    return Div(
        P("Ring loader", cls=combine_classes(font_weight.semibold, m.b(1))),
        P("Loaded successfully!"),
        id="ring-demo",
        cls=combine_classes(card, card_body, bg_dui.base_100)
    )

@rt("/async_loading/content/ball")
def async_content_ball():
    """Return loaded content for ball example."""
    import time
    time.sleep(0.8)
    return Div(
        P("Ball loader", cls=combine_classes(font_weight.semibold, m.b(1))),
        P("Loaded successfully!"),
        id="ball-demo",
        cls=combine_classes(card, card_body, bg_dui.base_100)
    )

@rt("/async_loading/content/inner")
def async_content_inner():
    """Return loaded content for innerHTML swap example."""
    import time
    time.sleep(1)
    # Note: No ID needed since we're swapping innerHTML
    return Div(
        H3("Inner Content", cls=combine_classes(font_size.xl, font_weight.bold, m.b(2))),
        P("This content replaced only the inner HTML of the container."),
        P("The container div with its styling and ID persisted."),
        P(f"Loaded at: {time.strftime('%H:%M:%S')}")
    )

@rt
def modal_dialogs(request):
    """Modal dialog patterns demo page."""
    import time

    def modal_content():
        # Create modals for different examples

        # Example 1: Simple info modal
        simple_modal = ModalDialog(
            modal_id="info",
            content=Div(
                H2("Information", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("This is a simple informational modal with default settings.", cls=str(m.b(4))),
                P("Click the X button or the backdrop to close.", cls=combine_classes(text_align.center)),
                cls=combine_classes(card_body)
            ),
            size=ModalSize.SMALL
        )

        # Example 2: Large modal with async content
        loading_modal = ModalDialog(
            modal_id="settings",
            content=AsyncLoadingContainer(
                container_id="settings-form",
                load_url="/modal_dialogs/content/settings",
                loading_message="Loading settings..."
            ),
            size=ModalSize.LARGE
        )

        # Example 3: Full-screen modal
        fullscreen_modal = ModalDialog(
            modal_id="media",
            content=Div(
                H2("Full Screen Modal", cls=combine_classes(font_size._3xl, font_weight.bold, m.b(4), text_align.center)),
                Div(
                    P("This modal takes up most of the screen (11/12 width and height).", cls=combine_classes(m.b(4))),
                    P("Perfect for displaying media, galleries, or detailed content.", cls=combine_classes(m.b(4))),
                    Div(
                        Div(cls=combine_classes(card, bg_dui.base_200, p(16))),
                        cls=combine_classes(grid_display, grid_cols._2, gap._4)
                    ),
                    cls=combine_classes(flex_display, items.center, justify.center, h.full)
                ),
                cls=combine_classes(card_body)
            ),
            size=ModalSize.FULL
        )

        # Example 4: Custom size modal with auto-show
        welcome_modal = ModalDialog(
            modal_id="welcome",
            content=Div(
                H2("Welcome! 👋", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4), text_align.center)),
                P("This modal appeared automatically when the page loaded.", cls=combine_classes(text_align.center, m.b(2))),
                P("Close it and refresh the page to see it again!", cls=combine_classes(text_align.center)),
                cls=combine_classes(card_body)
            ),
            size=ModalSize.CUSTOM,
            custom_width=str(w("96")),
            custom_height=str(h("48")),
            auto_show=True
        )

        # Example 5: Modal with HTMX form
        form_modal = ModalDialog(
            modal_id="contact",
            content=Div(
                H2("Contact Form", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                Form(
                    Div(
                        Label("Name:", cls=combine_classes(font_weight.semibold, m.b(2))),
                        Input(
                            name="name",
                            placeholder="Your name",
                            required=True,
                            cls=combine_classes(text_input, w.full, m.b(4))
                        )
                    ),
                    Div(
                        Label("Email:", cls=combine_classes(font_weight.semibold, m.b(2))),
                        Input(
                            name="email",
                            type="email",
                            placeholder="your@email.com",
                            required=True,
                            cls=combine_classes(text_input, w.full, m.b(4))
                        )
                    ),
                    Div(
                        Label("Message:", cls=combine_classes(font_weight.semibold, m.b(2))),
                        Textarea(
                            name="message",
                            placeholder="Your message",
                            required=True,
                            rows=4,
                            cls=combine_classes(text_input, w.full, m.b(4))
                        )
                    ),
                    Div(
                        Button(
                            "Send Message",
                            type="submit",
                            cls=combine_classes(btn, btn_colors.primary, m.r(2))
                        ),
                        Button(
                            "Cancel",
                            type="button",
                            onclick=f"document.getElementById('{InteractionHtmlIds.modal_dialog('contact')}').close()",
                            cls=combine_classes(btn, btn_styles.ghost)
                        ),
                        cls=combine_classes(text_align.right)
                    ),
                    hx_post="/modal_dialogs/submit/contact",
                    hx_target=f"#{InteractionHtmlIds.modal_dialog_content('contact')}",
                    hx_swap="innerHTML"
                ),
                id=InteractionHtmlIds.modal_dialog_content("contact"),
                cls=combine_classes(card_body)
            ),
            size=ModalSize.MEDIUM
        )

        return Div(
            H1("Modal Dialog Pattern",
               cls=combine_classes(font_size._3xl, font_weight.bold, m.b(6), text_align.center)),

            P("The ModalDialog pattern provides reusable modal dialogs with DaisyUI styling.",
              cls=combine_classes(text_align.center, m.b(8), max_w._3xl, m.x.auto)),

            # Example 1: Simple modal
            Div(
                H2("Example 1: Simple Info Modal",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("Basic modal with default settings (small size)",
                  cls=combine_classes(m.b(4))),
                ModalTriggerButton(
                    modal_id="info",
                    label="Show Info Modal",
                    button_cls=str(btn_colors.info)
                ),
                cls=str(m.b(8))
            ),

            # Example 2: Large modal with async content
            Div(
                H2("Example 2: Large Modal with Async Content",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("Modal that loads content asynchronously using AsyncLoadingContainer",
                  cls=combine_classes(m.b(4))),
                ModalTriggerButton(
                    modal_id="settings",
                    label="Open Settings",
                    button_cls=str(btn_colors.primary)
                ),
                cls=str(m.b(8))
            ),

            # Example 3: Full-screen modal
            Div(
                H2("Example 3: Full-Screen Modal",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("Modal that takes up most of the screen (11/12 width and height)",
                  cls=combine_classes(m.b(4))),
                ModalTriggerButton(
                    modal_id="media",
                    label="View Full Screen",
                    button_cls=str(btn_colors.secondary)
                ),
                cls=str(m.b(8))
            ),

            # Example 4: Auto-show modal (welcome)
            Div(
                H2("Example 4: Auto-Show Modal",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("This modal appeared automatically when you loaded this page. Refresh to see it again!",
                  cls=combine_classes(m.b(4))),
                P("(Custom size with auto_show=True parameter)",
                  cls=combine_classes(m.b(4))),
                cls=str(m.b(8))
            ),

            # Example 5: Modal with form
            Div(
                H2("Example 5: Modal with Form",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("Modal containing a form that submits via HTMX",
                  cls=combine_classes(m.b(4))),
                ModalTriggerButton(
                    modal_id="contact",
                    label="Contact Us",
                    button_cls=str(btn_colors.success)
                ),
                cls=str(m.b(8))
            ),

            # Render all modals
            simple_modal,
            loading_modal,
            fullscreen_modal,
            welcome_modal,
            form_modal,

            cls=combine_classes(
                container,
                max_w._6xl,
                m.x.auto,
                p(8)
            )
        )

    return handle_htmx_request(
        request,
        modal_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
    )

# Modal dialog content endpoints
@rt("/modal_dialogs/content/settings")
def modal_content_settings():
    """Return settings form content after delay."""
    import time
    time.sleep(1)
    return Div(
        H2("Settings Configuration", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
        P("Configure your application preferences:", cls=combine_classes(m.b(4))),

        Div(
            Label("Theme:", cls=combine_classes(font_weight.semibold, m.b(2))),
            Select(
                Option("Light", value="light"),
                Option("Dark", value="dark"),
                Option("Cupcake", value="cupcake"),
                Option("Forest", value="forest"),
                cls=combine_classes(select, w.full)
            ),
            cls=str(m.b(4))
        ),

        Div(
            Label("Notifications:", cls=combine_classes(font_weight.semibold, m.b(2))),
            Select(
                Option("All", value="all"),
                Option("Important only", value="important"),
                Option("None", value="none"),
                cls=combine_classes(select, w.full)
            ),
            cls=str(m.b(4))
        ),

        Div(
            Button("Save Settings", cls=combine_classes(btn, btn_colors.primary, m.r(2))),
            Button("Cancel", onclick=f"document.getElementById('{InteractionHtmlIds.modal_dialog('settings')}').close()",
                   cls=combine_classes(btn, btn_styles.ghost)),
            cls=combine_classes(text_align.right)
        ),

        id="settings-form"
    )

@rt("/modal_dialogs/submit/contact")
def modal_submit_contact(name: str, email: str, message: str):
    """Handle contact form submission."""
    import time
    time.sleep(0.5)
    return Div(
        H2("Message Sent! ✓", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4), text_align.center)),
        P(f"Thank you, {name}!", cls=combine_classes(text_align.center, m.b(2))),
        P(f"We've received your message and will respond to {email} soon.",
          cls=combine_classes(text_align.center, m.b(4))),
        Div(
            Button(
                "Close",
                onclick=f"document.getElementById('{InteractionHtmlIds.modal_dialog('contact')}').close()",
                cls=combine_classes(btn, btn_colors.primary)
            ),
            cls=combine_classes(text_align.center)
        ),
        id=InteractionHtmlIds.modal_dialog_content("contact")
    )

@rt
def sse_monitor(request):
    """SSE connection monitor patterns demo page."""
    import time
    import random

    def sse_content():
        connection_id = "demo"

        # Create connection monitor with custom configuration
        config = SSEConnectionConfig(
            max_reconnect_attempts=5,
            reconnect_delay=1000,
            max_backoff_multiplier=3,
            log_to_console=True
        )

        status_container, monitor_script = SSEConnectionMonitor(
            connection_id=connection_id,
            status_size="sm",
            config=config
        )

        return Div(
            H1("SSE Connection Monitor Pattern",
               cls=combine_classes(font_size._3xl, font_weight.bold, m.b(6), text_align.center)),

            P("The SSE Connection Monitor pattern provides visual status indicators and automatic reconnection for Server-Sent Events.",
              cls=combine_classes(text_align.center, m.b(8), max_w._3xl, m.x.auto)),

            # Example 1: Live connection monitor
            Div(
                H2("Example 1: Live Connection Monitor",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("This example shows a real SSE connection with live updates. The status indicator shows the connection state.",
                  cls=combine_classes(m.b(4))),

                # Connection status card
                Div(
                    Div(
                        Div(
                            H3("Connection Status", cls=combine_classes(font_weight.semibold, m.b(2))),
                            status_container,
                            cls=combine_classes(flex_display, items.center, justify.between)
                        ),
                        cls=combine_classes(card_body, m.b(4))
                    ),

                    # Live updates display
                    Div(
                        H3("Live Updates", cls=combine_classes(font_weight.semibold, m.b(2))),
                        Div(
                            P("Waiting for updates...", cls=combine_classes(text_align.center, p(4))),
                            hx_ext="sse",
                            sse_connect="/stream/sse_monitor",
                            sse_swap="update",
                            id=InteractionHtmlIds.sse_element(connection_id),
                            cls=str(combine_classes(card_body, bg_dui.base_200))
                        ),
                        cls=combine_classes(card_body)
                    ),

                    cls=combine_classes(card, bg_dui.base_100)
                ),

                cls=str(m.b(8))
            ),

            # Example 2: Features
            Div(
                H2("Features",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                Div(
                    Div(
                        H3("Visual Status Indicators", cls=combine_classes(font_weight.semibold, m.b(2))),
                        Ul(
                            Li("Live - Connected and receiving updates"),
                            Li("Disconnected - Connection lost, not reconnecting"),
                            Li("Error - Connection error occurred"),
                            Li("Reconnecting - Attempting to reconnect"),
                            cls=combine_classes(m.l(6))
                        ),
                        cls=combine_classes(card_body)
                    ),
                    Div(
                        H3("Automatic Reconnection", cls=combine_classes(font_weight.semibold, m.b(2))),
                        Ul(
                            Li("Exponential backoff strategy"),
                            Li("Configurable retry attempts"),
                            Li("Configurable delay and backoff"),
                            Li("Graceful degradation"),
                            cls=combine_classes(m.l(6))
                        ),
                        cls=combine_classes(card_body)
                    ),
                    Div(
                        H3("Smart Behavior", cls=combine_classes(font_weight.semibold, m.b(2))),
                        Ul(
                            Li("Tab visibility awareness"),
                            Li("Server shutdown detection"),
                            Li("OOB swap detection"),
                            Li("Console logging (optional)"),
                            cls=combine_classes(m.l(6))
                        ),
                        cls=combine_classes(card_body)
                    ),
                    cls=combine_classes(grid_display, grid_cols._1, grid_cols._3.md, gap._4, m.b(6))
                ),
                cls=str(m.b(8))
            ),

            # Example 3: Configuration
            Div(
                H2("Configuration Options",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("Customize the connection monitor behavior with SSEConnectionConfig:",
                  cls=combine_classes(m.b(4))),
                Div(
                    Code("""config = SSEConnectionConfig(
    max_reconnect_attempts=5,    # Max retry attempts
    reconnect_delay=1000,         # Initial delay (ms)
    max_backoff_multiplier=3,     # Max backoff multiplier
    monitor_visibility=True,      # Monitor tab visibility
    log_to_console=True           # Enable logging
)""", cls=combine_classes(
                        "whitespace-pre",
                        "block",
                        p(4),
                        bg_dui.base_200,
                        "rounded"
                    )),
                    cls=combine_classes(card, card_body, bg_dui.base_100)
                ),
                cls=str(m.b(8))
            ),

            # Monitor script (required)
            monitor_script,

            cls=combine_classes(
                container,
                max_w._6xl,
                m.x.auto,
                p(8)
            )
        )

    return handle_htmx_request(
        request,
        sse_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
    )

# SSE streaming endpoint
@rt("/stream/sse_monitor")
async def stream_sse_monitor():
    """SSE endpoint for connection monitor demo."""
    import asyncio
    import time
    from starlette.responses import StreamingResponse

    async def event_generator():
        try:
            counter = 0
            while counter < 20:  # Stream 20 updates then stop
                counter += 1
                timestamp = time.strftime('%H:%M:%S')

                # Generate update content
                progress_value = min(counter * 5, 100)
                update_content = Div(
                    H4(f"Update #{counter}", cls=combine_classes(font_weight.bold, m.b(2))),
                    P(f"Received at: {timestamp}", cls=str(m.b(1))),
                    P(f"Status: Streaming ({counter}/20 updates)", cls=str(m.b(2))),
                    Progress(
                        value=str(progress_value),
                        max="100",
                        cls=combine_classes(progress, progress_colors.primary, w.full)
                    ),
                    cls=combine_classes(p(4))
                )

                # Send SSE event
                yield f"event: update\n"
                yield f"data: {str(update_content)}\n\n"

                # Wait before next update
                await asyncio.sleep(2)

            # Final update
            final_content = Div(
                H4("Stream Complete ✓", cls=combine_classes(font_weight.bold, m.b(2), text_align.center)),
                P("All 20 updates delivered successfully.", cls=combine_classes(text_align.center, m.b(2))),
                P("Refresh the page to see the stream again.", cls=combine_classes(text_align.center)),
                cls=combine_classes(p(4), bg_dui.success, "text-success-content", "rounded")
            )
            yield f"event: update\n"
            yield f"data: {str(final_content)}\n\n"

        except asyncio.CancelledError:
            # Send close message before shutting down
            yield f"event: close\n"
            yield f"data: Server shutting down\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )

@rt
def pagination_demo(request, page: int = 1, example: str = None):
    """Pagination controls patterns demo page."""

    # Sample data for demonstration
    total_items = 100
    items_per_page = 10
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # Calculate items for current page
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    current_items = list(range(start_idx + 1, end_idx + 1))

    # If this is an HTMX request for a specific example, return only that example's content
    if example == "1":
        # Helper function to generate route for page (example 1)
        def make_route_ex1(p: int) -> str:
            return f"/pagination_demo?page={p}&example=1"

        return Div(
            # Header
            Div(
                H3("Item List", cls=combine_classes(font_weight.semibold, m.b(2))),
                P(f"Showing items {start_idx + 1}-{end_idx} of {total_items}",
                  cls=combine_classes(m.b(4))),
                cls=combine_classes(card_body, bg_dui.base_200)
            ),

            # Items grid
            Div(
                *[
                    Div(
                        Div(
                            H4(f"Item #{item}", cls=combine_classes(font_weight.bold, m.b(2))),
                            P(f"This is item number {item} in the list.", cls=combine_classes(m.b(2))),
                            P(f"Page {page} of {total_pages}", cls=combine_classes(font_size.sm)),
                            cls=combine_classes(card_body)
                        ),
                        cls=combine_classes(card, bg_dui.base_100)
                    )
                    for item in current_items
                ],
                cls=combine_classes(grid_display, grid_cols._1, grid_cols._2.md, grid_cols._3.lg, gap._4, m.b(6))
            ),

            # Pagination controls
            PaginationControls(
                current_page=page,
                total_pages=total_pages,
                route_func=make_route_ex1,
                target_id="pagination-content-1"
            ),

            id="pagination-content-1",
            cls=combine_classes(card, bg_dui.base_100, p(6))
        )

    elif example == "2":
        # Helper function to generate route for page (example 2)
        def make_route_ex2(p: int) -> str:
            return f"/pagination_demo?page={p}&example=2"

        return Div(
            Div(
                H3("Results List", cls=combine_classes(font_weight.semibold, m.b(4))),
                Ul(
                    *[Li(f"Result item {i} (Page {page})", cls=str(m.b(2))) for i in range(1, 6)],
                    cls=combine_classes(m.l(6), m.b(6))
                ),
                cls=combine_classes(card_body)
            ),

            # Compact pagination (no page info)
            PaginationControls(
                current_page=page,
                total_pages=total_pages,
                route_func=make_route_ex2,
                target_id="pagination-content-2",
                style=PaginationStyle.COMPACT
            ),

            id="pagination-content-2",
            cls=combine_classes(card, bg_dui.base_100, p(6))
        )

    elif example == "3":
        # Helper function to generate route for page (example 3)
        def make_route_ex3(p: int) -> str:
            return f"/pagination_demo?page={p}&example=3"

        return Div(
            Div(
                H3("Search Results", cls=combine_classes(font_weight.semibold, m.b(2))),
                P(f"Custom button text and smaller size (Page {page})", cls=combine_classes(m.b(4))),
                cls=combine_classes(card_body)
            ),

            # Custom styled pagination
            PaginationControls(
                current_page=page,
                total_pages=total_pages,
                route_func=make_route_ex3,
                target_id="pagination-content-3",
                prev_text="← Back",
                next_text="Forward →",
                button_size=str(btn_sizes.sm),
                page_info_format="{current}/{total}"
            ),

            id="pagination-content-3",
            cls=combine_classes(card, bg_dui.base_100, p(6))
        )

    # Otherwise, return the full demo page
    def pagination_content():
        # Helper function to generate route for page (example 1)
        def make_route_ex1(p: int) -> str:
            return f"/pagination_demo?page={p}&example=1"

        # Helper function to generate route for page (example 2)
        def make_route_ex2(p: int) -> str:
            return f"/pagination_demo?page={p}&example=2"

        # Helper function to generate route for page (example 3)
        def make_route_ex3(p: int) -> str:
            return f"/pagination_demo?page={p}&example=3"

        return Div(
            H1("Pagination Controls Pattern",
               cls=combine_classes(font_size._3xl, font_weight.bold, m.b(6), text_align.center)),

            P("The PaginationControls pattern provides navigation between pages of content with HTMX integration.",
              cls=combine_classes(text_align.center, m.b(8), max_w._3xl, m.x.auto)),

            # Example 1: Simple pagination with paginated content
            Div(
                H2("Example 1: Simple Pagination",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("Default pagination style with page info display",
                  cls=combine_classes(m.b(4))),

                # Content container that gets updated
                Div(
                    # Header
                    Div(
                        H3("Item List", cls=combine_classes(font_weight.semibold, m.b(2))),
                        P(f"Showing items {start_idx + 1}-{end_idx} of {total_items}",
                          cls=combine_classes(m.b(4))),
                        cls=combine_classes(card_body, bg_dui.base_200)
                    ),

                    # Items grid
                    Div(
                        *[
                            Div(
                                Div(
                                    H4(f"Item #{item}", cls=combine_classes(font_weight.bold, m.b(2))),
                                    P(f"This is item number {item} in the list.", cls=combine_classes(m.b(2))),
                                    P(f"Page {page} of {total_pages}", cls=combine_classes(font_size.sm)),
                                    cls=combine_classes(card_body)
                                ),
                                cls=combine_classes(card, bg_dui.base_100)
                            )
                            for item in current_items
                        ],
                        cls=combine_classes(grid_display, grid_cols._1, grid_cols._2.md, grid_cols._3.lg, gap._4, m.b(6))
                    ),

                    # Pagination controls
                    PaginationControls(
                        current_page=page,
                        total_pages=total_pages,
                        route_func=make_route_ex1,
                        target_id="pagination-content-1"
                    ),

                    id="pagination-content-1",
                    cls=combine_classes(card, bg_dui.base_100, p(6))
                ),
                cls=str(m.b(8))
            ),

            # Example 2: Compact pagination
            Div(
                H2("Example 2: Compact Pagination",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("Compact style without page info (Previous/Next only)",
                  cls=combine_classes(m.b(4))),

                Div(
                    Div(
                        H3("Results List", cls=combine_classes(font_weight.semibold, m.b(4))),
                        Ul(
                            *[Li(f"Result item {i} (Page {page})", cls=str(m.b(2))) for i in range(1, 6)],
                            cls=combine_classes(m.l(6), m.b(6))
                        ),
                        cls=combine_classes(card_body)
                    ),

                    # Compact pagination (no page info)
                    PaginationControls(
                        current_page=page,
                        total_pages=total_pages,
                        route_func=make_route_ex2,
                        target_id="pagination-content-2",
                        style=PaginationStyle.COMPACT
                    ),

                    id="pagination-content-2",
                    cls=combine_classes(card, bg_dui.base_100, p(6))
                ),
                cls=str(m.b(8))
            ),

            # Example 3: Custom styling
            Div(
                H2("Example 3: Custom Styling",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                P("Pagination with custom button text and size",
                  cls=combine_classes(m.b(4))),

                Div(
                    Div(
                        H3("Search Results", cls=combine_classes(font_weight.semibold, m.b(2))),
                        P(f"Custom button text and smaller size (Page {page})", cls=combine_classes(m.b(4))),
                        cls=combine_classes(card_body)
                    ),

                    # Custom styled pagination
                    PaginationControls(
                        current_page=page,
                        total_pages=total_pages,
                        route_func=make_route_ex3,
                        target_id="pagination-content-3",
                        prev_text="← Back",
                        next_text="Forward →",
                        button_size=str(btn_sizes.sm),
                        page_info_format="{current}/{total}"
                    ),

                    id="pagination-content-3",
                    cls=combine_classes(card, bg_dui.base_100, p(6))
                ),
                cls=str(m.b(8))
            ),

            # Example 4: Features overview
            Div(
                H2("Features",
                   cls=combine_classes(font_size._2xl, font_weight.bold, m.b(4))),
                Div(
                    Div(
                        H3("Navigation", cls=combine_classes(font_weight.semibold, m.b(2))),
                        Ul(
                            Li("Previous/Next buttons"),
                            Li("Automatic disabled states"),
                            Li("Current page display"),
                            Li("HTMX integration"),
                            cls=combine_classes(m.l(6))
                        ),
                        cls=combine_classes(card_body)
                    ),
                    Div(
                        H3("Customization", cls=combine_classes(font_weight.semibold, m.b(2))),
                        Ul(
                            Li("Custom button text"),
                            Li("Page info format"),
                            Li("Button sizes"),
                            Li("Multiple styles"),
                            cls=combine_classes(m.l(6))
                        ),
                        cls=combine_classes(card_body)
                    ),
                    Div(
                        H3("Integration", cls=combine_classes(font_weight.semibold, m.b(2))),
                        Ul(
                            Li("SPA-like navigation"),
                            Li("URL management"),
                            Li("Target swapping"),
                            Li("Flexible routing"),
                            cls=combine_classes(m.l(6))
                        ),
                        cls=combine_classes(card_body)
                    ),
                    cls=combine_classes(grid_display, grid_cols._1, grid_cols._3.md, gap._4, m.b(6))
                ),
                cls=str(m.b(8))
            ),

            cls=combine_classes(
                container,
                max_w._6xl,
                m.x.auto,
                p(8)
            )
        )

    return handle_htmx_request(
        request,
        pagination_content,
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
        ("Async Loading", async_loading),
        ("Modal Dialog", modal_dialogs),
        ("SSE Monitor", sse_monitor),
        ("Pagination", pagination_demo),
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
print("  • PaginationControls - Navigation controls for paginated content")
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
    print(f"  http://{display_host}:{port}/async_loading     - AsyncLoadingContainer demo")
    print(f"  http://{display_host}:{port}/modal_dialogs     - ModalDialog demo")
    print(f"  http://{display_host}:{port}/sse_monitor       - SSEConnectionMonitor demo")
    print(f"  http://{display_host}:{port}/pagination_demo   - PaginationControls demo")
    print(f"  http://{display_host}:{port}/features          - Feature list")
    print("\n" + "="*70 + "\n")

    # Open browser after a short delay
    timer = threading.Timer(1.5, lambda: open_browser(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    # Start server
    uvicorn.run(app, host=host, port=port)
