#%%
# this is meant to be run in vscode
import solution_test
import matplotlib.pyplot as plt
#%load_ext autoreload
#%autoreload 2
#%%
sols = solution_test.main(5, root=0)

#%%
solution_test.vis_sol(sols[0])
#%%
solution_test.vis_sol(sols[4])

#%%
# refresh
import importlib
importlib.reload(solution_test)