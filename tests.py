import datamanager
dm = datamanager.DataManager(r'G:\Dropbox\openpipe\BaseTestProject\New_Project')

try:
    shot = dm.new_shot('tst0010', 0, 100)
except:
    shot = dm.get_shot_or_asset('tst0010')
# shot.create_task_dir('model')

shot.create_new_take("G:\\Dropbox\\openpipe\\BaseTestProject\\New_Project\\scenes\\tst0010\\model\\scene.json")