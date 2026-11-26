#!/usr/bin/env python
# coding: utf-8

# # Employee Data Analysis
# 
# ## NumPy Student Marks

# In[1]:


import sys
from pathlib import Path

PROJECT_ROOT = Path.cwd()
if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent

sys.path.insert(0, str(PROJECT_ROOT / "src"))
import task3


# In[2]:


task3.numpy_examples()


# ## Employee Data Cleaning, Summary, and Charts

# In[3]:


task3.make_department_file()
employees = task3.load_and_clean_employees()
summary = task3.summarize_and_merge(employees)
task3.make_charts(employees, summary)


# ## Timing

# In[4]:


get_ipython().run_line_magic('timeit', 'employees["salary"].mean()')


# 
