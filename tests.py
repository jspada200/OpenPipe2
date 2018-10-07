import datamanager
dm = datamanager.DataManager(r'G:\Dropbox\openpipe\BaseTestProject\New_Project')

try:
    asset = dm.new_asset('giacomo')
except:
    asset = dm.get_shot_or_asset('giacomo')
asset.create_task_dir('rig')

# shot.create_new_take("G:\\Dropbox\\openpipe\\BaseTestProject\\New_Project\\scenes\\tst0010\\model\\scene.json")