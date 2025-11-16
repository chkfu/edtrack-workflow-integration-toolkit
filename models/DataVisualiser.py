import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#  CLASS

class DataVisualiser:
  
  def __init__ (self):
    print("[DataVisualiser] initialised successfully.")
    
    
  #  METHODS  -  DRAWING
  
  def draw_heatmap(self, 
                   target_df: pd.DataFrame,
                   target_title: str = "Untitled",
                   target_xlabel: str = "x_axis",
                   target_ylabel: str = "y_axis",
                   target_vmin: int = 0,
                   target_vmax: int = 100):
    try:
      #  diagram size
      plt.figure(figsize=(12, 10))
      
      #  heatmap details
      axes= sns.heatmap(data=target_df,
                        annot=True,
                        annot_kws={"size": 8},
                        fmt=".0f",
                        linewidth=0.5,
                        vmin=target_vmin, 
                        vmax=target_vmax,
                        cmap="cividis")
      axes.set_title(target_title, 
                     fontsize=14, 
                     fontweight="bold", 
                     pad=16)
      axes.set(xlabel=target_xlabel, 
               ylabel=target_ylabel)
      
      #  heatmap drawing
      plt.xticks(fontsize=8)
      plt.yticks(fontsize=8)
      plt.tight_layout()
    
      figure = axes.get_figure()
      return figure, axes
    
    except Exception as ex:
      raise Exception(f"[Error] failed to draw heatmap: {ex}")
    