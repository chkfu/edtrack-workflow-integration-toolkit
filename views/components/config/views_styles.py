THEME_COLOR = {
    "dark":    "#333333",
    "primary": "#213D57",
    "mid":     "#334C64",
    "light":   "#475F76",
    "pale":    "#C6D1D8",
    "gray":    "#999999",
    "white":   "#FFFFFF",
    "yellow": "#fab005",
    "red": "#FA5252",
    "primary_hvr": "#455C75",
    "mid_hvr": "#293D50",
    "pale_hvr": "#B0BCC3",
    "white_hvr":   "#DDDDDD",
    "yellow_hvr": "#F08C00",
    "red_hvr": "#E03131"
}



#  WINDOW

style_wd_default = {
  "title": "EdTrack 🧭",
  "resolution_width": 720,
  "resolution_height": 640,
  "f_fam": "Arial",
  "f_size": 12,
}

style_wd_default_2 = """
  QWidget {{
      background-color: {pale};
      color: {primary};
  }}
""".format(
    primary=THEME_COLOR["primary"],
    pale=THEME_COLOR["pale"]
)


#  LAYER 1 - TOPBAR

style_topbar_default = """
  QFrame {{
      background-color: {primary};
      color: {dark};
      padding: 0px;
      margin: 0px;
  }}
  """.format(
      primary=THEME_COLOR["primary"],
      dark=THEME_COLOR["dark"]
  )



#  LAYER 2 - SIDEBAR
style_sidebar_box_default = """
  QWidget {{
      background-color: {white_hvr};
      color: {primary};
      padding: 0px;
      margin: 0px;
  }}
  """.format(
      white_hvr=THEME_COLOR["white_hvr"],
      primary=THEME_COLOR["primary"])
  
  
style_table_view_border = """
QTableView {{
    border: 0.5px solid {dark};
}}
""".format(
  dark=THEME_COLOR["dark"]
)



#  LAYER 2 - CONTENT PANEL

style_content_panel_default = """
  QWidget {{
    padding: 4px;
    }}
  """
  
  
#  LAYER 3 - NAVIGATION SECTION

style_nav_sect_default = """
  QWidget {{
    padding: 4px;
    }}
  
  """
  
#  LAYER 4 - PAGES

style_tab_border = """
    QTabWidget {
        background: transparent;
        border: none;
    }
    QTabWidget::pane {
        background: transparent;
        border: none;
    }
    """

style_tab_scroll = """
QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    width: 4px;
    background: transparent;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: {primary};
    min-height: 16px;
    border-radius: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background: {primary_hvr};
}}

QScrollBar::add-line,
QScrollBar::sub-line {{
    height: 0px;
}}
""".format(
    primary=THEME_COLOR["primary"],
    primary_hvr=THEME_COLOR["primary_hvr"],
)

style_browser_box_pframe = """
QFrame {{
    background-color: {pale};
    border-radius: 14px;
    padding: 0px 4px;
}}
""".format(
    pale=THEME_COLOR["pale_hvr"]
)

#  LAYER 6 - POPUP WINDOW

style_popup_title_box = """
    background-color: {primary};
    padding: 12px;
""".format(
    primary=THEME_COLOR["primary"],
)


#  LABELS

style_lb_default = """
QLabel {{
  color: {txtcolor};
}}
"""

style_sidebar_listItem_default = """
QLabel {{
  color: {txtcolor};
  background-color: {bgcolor};
  padding: 8px 8px;
}}
"""


#  DROPDOWN

style_dd_default = """
QComboBox QAbstractItemView::item {
  height: 34px;
  padding-left: 10px;
  cursor: pointing-hand;
}
"""


#  BUTTONS

style_btn_default = """
  QPushButton {{
    background-color: {bgcolor};
    color: {txtcolor};
    border: 1px solid {bgcolor};
    border-radius: 14px;
    margin: 0px 0px;
    padding: 4px 8px;
    font-family: "Impact";
    font-size: 14px;
  }}
  QPushButton:hover {{
    background-color: {hover_bgcolor};
  }}
  QPushButton:pressed {{
      background-color: {bgcolor};
      border: 1px solid {txtcolor};
}}
"""

style_btn_contrast = """
QPushButton {{
    background-color: {bgcolor};
    color: {txtcolor};
    border: 1px solid {txtcolor};
    border-radius: 14px;
    margin: 0;
    padding: 4px 8px;
    font-family: "Impact";
    font-size: 14px;
}}
QPushButton:hover {{
    background-color: {hover_bgcolor};
}}
QPushButton:pressed {{
    background-color: {bgcolor};
    border: 1px solid {txtcolor};
}}
"""


