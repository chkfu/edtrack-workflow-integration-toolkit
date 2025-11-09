THEME_COLOR = {
    "dark":    "#333333",
    "primary": "#213D57",
    "mid":     "#334C64",
    "light":   "#475F76",
    "pale":    "#C6D1D8",
    "gray":    "#999999",
    "white":   "#ffffff",
    "primary_hvr": "#455C75",
    "white_hvr":   "#dddddd"
}



#  WINDOW

style_wd_default = {
  "title": "EduTrack 🧭",
  "resolution_width": 720,
  "resolution_height": 600,
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
      border: 1px solid {gray};
      color: {primary};
      padding: 0px;
      margin: 0px;
  }}
  """.format(
      white_hvr=THEME_COLOR["white_hvr"],
      gray=THEME_COLOR["gray"],
      primary=THEME_COLOR["primary"])


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
  border: 1px solid {txtcolor};
  padding: 8px;
}}
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
    font-family: "Arial";
    font-size: 12px;
    font-weight: 500;
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
    font-family: "Arial";
    font-size: 12px;
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: {hover_bgcolor};
}}
QPushButton:pressed {{
    background-color: {bgcolor};
    border: 1px solid {txtcolor};
}}
"""



#  TESTING

style_testing_border = """
    border: 1px solid red;
"""