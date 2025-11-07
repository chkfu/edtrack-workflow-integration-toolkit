#  WINDOW

style_wd_default = {
  "title": "EduTrack",
  "resolution_width": 600,
  "resolution_height": 600,
  "f_fam": "Arial",
  "f_size": 12
}

style_wd_default_2 = """
  QWidget {
      border: 1px solid black;
      background-color: #f8f9fa;
      color: #212529;
  }
"""


#  TOPBAR

style_topbar_default = """
  QFrame {
      border: 1px solid black;
      background-color: #14213d;
      color: #212529;
      padding: 0px;
      margin: 0px;
  }
"""


#  BUTTONS


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




style_btn_default = """
  QPushButton {{
    background-color: {bgcolor};
    color: {txtcolor};
    width: 60px;
    border: none;
    border-radius: 14px;
    margin: 0px 0px;
    padding: 4px 8px;
    font-family: "Segoe UI", "Helvetica Neue", "Arial", sans-serif;
    font-size: 12px;
    font-weight: 500;
  }}
  QPushButton:hover {{
    background-color: {hover_bgcolor};
  }}
"""



