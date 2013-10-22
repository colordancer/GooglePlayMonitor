# coding:utf-8

import os
# import MySQLdb
from hashlib import md5

#conn = MySQLdb.connect('127.0.0.1', 'root', 'abcd!@#$', 'googleplaycrawler')
conn = 0
ROOT = os.getcwd()
storeRootPath = "e:\\crawler\\GooglePlayCrawler\\apk\\"

class APK:
	def __init__(self):
		self.package_name = ''
		self.package_name_md5 = ''
		self.app_name = ''
		self.app_name_md5 = ''
		self.creator = ''
		self.creator_md5 = ''
		self.size = 0
		self.md5 = ''
		self.file_name = ''
		

	def _checkApkExistApkInfo(self, package_name, app_name, size):
		self.package_name = package_name
		self.app_name = app_name
		self.size = int(size)
		
		cursor = conn.cursor()
		m = md5()
		m.update(package_name)
		self.package_name_md5 = m.hexdigest()
		m.update(app_name)
		self.app_name_md5 = m.hexdigest()
		
		count = cursor.execute("select * from t_apk where package_name_md5 = '%s' and app_name_md5 = '%s' and size = %d" % (self.package_name_md5, self.app_name_md5, self.size))
		cursor.close()
		if 0 < count:
			return 1
		return 0
		
	def _checkApkExistMd5(self, md5):
		self.md5 = md5
		cursor = conn.cursor()
		count = cursor.execute('select * from t_apk where md5 = "%s"' % md5)
		cursor.close()
		if 0 < count:
			return 1
		return 0

	def _isTrustedCreator(self, creator):
		self.creator = creator
		m = md5()
		m.update(creator)
		creator_md5 = m.hexdigest()
		self.creator_md5 = creator_md5
		
		cursor = conn.cursor()
		count = cursor.execute('select * from t_trusted_creator where creator_md5 ="%s"', creator_md5)
		cursor.close()
		if 0 < count:
			return 1
		return 0
	
	def _sqlEscape(self, src):
		src = src.replace('\\', '\\\\')
		src = src.replace('\'', '\\\'')
		src = src.replace('\"', '\\\"')
		src = src.replace('%', '\\%')
		src = src.replace('_', '\\_')
		return src
		
	def _insertDB(self):
		sqlFileName = self.file_name.replace('\\', '\\\\')
		from datetime import datetime
		now = datetime.now()
		cursor = conn.cursor()
		sql = "insert into t_apk(package_name, package_name_md5, app_name, app_name_md5, creator, creator_md5, size, file_path, md5, status, date_time)" \
			"values ('%s','%s', '%s','%s','%s','%s',%d,'%s','%s',%d,'%s')" % (self.package_name, self.package_name_md5, self._sqlEscape(self.app_name), self.app_name_md5, self._sqlEscape(self.creator), self.creator_md5, self.size, sqlFileName, self.md5, 1, now)
		count = cursor.execute(sql)
		cursor.close()
		conn.commit()
		return count
			
	def _filter(self, filePath, md5):
		if (self._checkApkExistMd5(md5)):
			return 0 
		return 1
	
	def _store(self, packageName, md5):
		fileName = packageName + "_" + md5 + ".apk"
		dirPath = storeRootPath + packageName
		if not os.path.exists(dirPath):
				os.makedirs(dirPath)
		filePath = dirPath + "\\" + fileName
		oldFilePath = ROOT + "\\" + packageName + ".apk"
		if not os.path.exists(filePath):
			os.rename(oldFilePath, filePath)
		self.file_name = fileName
		return filePath
	
	def _scan(self):
		return 0
	

		
	
	
if __name__ == '__main__':
	pass
