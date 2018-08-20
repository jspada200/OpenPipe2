import datamanager

dm = datamanager.DataManager(r'G:\Dropbox\openpipe\BaseTestProject\New_Project')
'''
dm.new_shot('tst0040', 0, 100)

shots = dm.get_shots()
print(shots)
'''

print(vars(dm.get_shot('tst0040')))
