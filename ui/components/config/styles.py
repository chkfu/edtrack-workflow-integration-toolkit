#  WINDOW

style_wd_default = {
  "title": "EduTrack 🧭",
  "resolution_width": 720,
  "resolution_height": 600,
  "f_fam": "Arial",
  "f_size": 12
}

style_wd_default_2 = """
  QWidget {
      background-color: #f8f9fa;
      color: #212529;
  }
"""


#  TOPBAR (GRID 1)

style_topbar_default = """
  QFrame {
      background-color: #14213d;
      color: #212529;
      padding: 0px;
      margin: 0px;
  }
"""


#  MAIN_AREA (GRID 2)




#  LABELS

style_lb_default_h1 = """
QLabel {{
  margin-left: 8px;
    font-size: 28px;
    font-weight: bold;
    color: {txtcolor};
    font-weight: 900;
    font-style: italic;
    font-family: "Impact", "Arial";
    letter-spacing: 0.7px;
}}
"""

style_lb_default_p = """
QLabel {{
    font-size: 13px;
    font-weight: normal;
    color: {txtcolor}
}}
"""



#  BUTTONS

style_btn_default = """
  QPushButton {{
    background-color: {bgcolor};
    color: {txtcolor};
    width: 60px;
    border: none;
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
"""



#  TESTING

style_testing_border = """
    border: 1px solid red;
"""