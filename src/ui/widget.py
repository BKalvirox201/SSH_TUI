from rich.panel import Panel
from abc import abstractmethod
from src.events.page_events import NavDirectionEnum

class Widget(Panel):
    def __init__(self,
     renderable,
     box = ...,
     *,
     title = None,
     title_align = "center",
     subtitle = None,
     subtitle_align = "center",
     safe_box = None,
     expand = True,
     style = "none",
     border_style = "none",
     width = None,
     height = None,
     padding = ...,
     highlight = False):
        super().__init__(renderable,
         box,
         title=title,
         title_align=title_align,
         subtitle=subtitle,
         subtitle_align=subtitle_align,
         safe_box=safe_box,
         expand=expand,
         style=style,
         border_style=border_style,
         width=width,
         height=height,
         padding=padding,
         highlight=highlight)

        self.is_highlighted: bool = False
        self.is_selected: bool = False

        #neighbouring panels for navigation
        self.north_panel: Widget | None = None
        self.east_panel: Widget | None = None
        self.south_panel: Widget | None = None
        self.west_panel: Widget | None = None

    @abstractmethod
    def set_neighbouring_widgets(        self,
        north_panel: Widget | None = None,
        east_panel: Widget | None = None,
        south_panel: Widget | None = None,
        west_panel: Widget | None = None,
        ):

        #neighbouring panels for navigation
        self.north_panel: Widget | None = north_panel
        self.east_panel: Widget | None = east_panel
        self.south_panel: Widget | None = south_panel
        self.west_panel: Widget | None = west_panel


    @abstractmethod
    def get_neighbouring_widget(self, direction: NavDirectionEnum) -> Widget:
        match direction:
            case NavDirectionEnum.NORTH:
                return self.north_panel
            case NavDirectionEnum.EAST:
                return self.east_panel
            case NavDirectionEnum.SOUTH:
                return self.south_panel
            case NavDirectionEnum.WEST:
                return self.west_panel
            case _:
                pass # Unreachable