STEP_NAME_LIST: list = [
    {
      "step": "1: Import Datasets", 
      "visited": True
    },
    {
      "step": "2: Clean Data", 
      "visited": False
    },
    {
      "step": "3: Merge Tables", 
      "visited": False
    },
    {
      "step": "4: Feature Engineering", 
      "visited": False
    },
    {
      "step": "5: Analyse Data", 
      "visited": False
    }
]


DATASET_LIST: list = [
  {
    "data": "MySQL Database", 
    "status": False
  },
  {
    "data": "Dataset - Users",
    "status": False
  },
  {
    "data": "Dataset - Activities",
    "status": False
  },
  {
    "data": "Dataset - Components",
    "status": False
  },
  {
    "data": "Dataset - Merged",
    "status": False
  }
]


RAW_COL_SCHEMA: dict = {
  "Dataset - Users": ["Date","Time", "User Full Name *Anonymized"],
  "Dataset - Activities": ["User Full Name *Anonymized", "Component", "Action", "Target"],
  "Dataset - Components": ["Component", "Code"]
}


#  PAGE SPEC CONFIGS


MERGE_METHOD_OPT: dict = {
  "left": "Keep all records from the left table.",
  "right": "Keep all records from the right table.",
  "inner": "Keep only records that match in both tables.",
  "outer": "Keep everything from both tables."
}