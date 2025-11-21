"""PaginationControls pattern demo - Navigation between pages with various styles."""

from demo import *

# Create APIRouter for pagination routes
pagination_ar = APIRouter(prefix="/pagination_demo")


@pagination_ar
def index(request, page: int = 1, example: str = None):
    """Pagination controls patterns demo page."""

    # Sample data for demonstration
    total_items = 100
    items_per_page = 10
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # Calculate items for current page
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    current_items = list(range(start_idx + 1, end_idx + 1))

    # If this is an HTMX request for a specific example's paginated content, return only that content
    if example == "1" and request.headers.get('HX-Request'):
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

    elif example == "2" and request.headers.get('HX-Request'):
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

    elif example == "3" and request.headers.get('HX-Request'):
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

    # Otherwise, return the full demo page (for all non-HTMX requests or no example parameter)
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

    from demo_app import navbar
    return handle_htmx_request(
        request,
        pagination_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
    )
