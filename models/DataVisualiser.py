import pandas as pd
import logging
import matplotlib.pyplot as plt
import seaborn as sns


#  LOGGING

logger = logging.getLogger("DATA_VISUALISER")


#  CLASS

class DataVisualiser:
  
  def __init__ (self):
    logger.info("initialised successfully.")
    
    
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
      logger.info("New correlation heatmap generated sucessfully.")
      return figure, axes
    
    except Exception as ex:
      logger.error(f"failed to draw heatmap: {ex}", exc_info=True)
      raise
    