"""
CopyMove.py

A script that move or copies info from one field and replaces or appends it to another field

Copyright Stonepaw 2013. Anyone is free to use all or any of this code as long as credit is given.

"""


import clr
import System
import datetime
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.IO import FileInfo, Path

from System.ComponentModel import BackgroundWorker
from System.Windows.Forms import *

from System.Drawing import *
import re
ICON = Path.Combine(FileInfo(__file__).DirectoryName, "Copy move.ico")
SETTINGS_FILE = Path.Combine(FileInfo(__file__).DirectoryName, "settings.dat")


#@Name Copy/Move Field
#@Hook Books
#@Image Copy move.png
def CopyMoveField(books):

	if books:
                settings = load_settings()
		f = CopyMoveFieldForm(books, settings)
		r = f.ShowDialog()

                settings["source_field"] = f._source.SelectedItem
                settings["destination_field"] = f._destination.SelectedItem
                settings["user_text"] = f._UserText.Text
                settings["seperator"] = f._seperator.Text
                if f._copy.Checked:                        
                        settings["source_mode"] = "Copy"
                elif f._move.Checked:
                        settings["source_mode"] = "Move"
                if f._replace.Checked:
                        settings["destination_mode"] = "Replace"
                elif f._append.Checked:
                        settings["destination_mode"] = "Append"		
		save_settings(settings)
		
	else:
		MessageBox.Show("No books selected")
		return


def save_settings(settings):
        try:
                with open(SETTINGS_FILE, 'w') as settings_file:
                        for key in settings:
                                if not settings[key]:
                                        continue
                                settings_file.write("%s:%s\n" %
                                                     (key, settings[key]))
        except IOError:
                print "Failed to writing settings file"


def load_settings():
        settings = {"source_field" : "Age Rating",
                    "destination_field" : "Age Rating",
                    "user_text" : "",
                    "source_mode" : "Copy",
                    "destination_mode" : "Replace",
                    "seperator" : "" }
        settings_lines = []
        try:
                with open(SETTINGS_FILE, 'r') as settings_file:
                        settings_lines = settings_file.readlines()

        except IOError:
                #No settings file  or other file error so return empty settings
                return settings
        if not settings_lines:
                return settings
        for line in settings_lines:
                print line
                match =  re.match("(?P<key>.*?):(?P<value>.+)", line)
                settings[match.group("key")] = match.group("value")
        return settings


class CopyMoveFieldForm(Form):
	def __init__(self, books, settings):
		self.InitializeComponent()

		self.books = books
		self.percentage = 1.0/len(books)*100
		self.progresspercent = 0.0
		self._source.SelectedItem = settings["source_field"]
		self._destination.SelectedItem = settings["destination_field"]
		if settings["source_mode"] == "Copy":
                        self._copy.Checked = True
                else:
                        self._move.Checked = True
                self._seperator.Text = settings["seperator"]
                self._UserText.Text = settings["user_text"]
                if settings["destination_mode"] == "Replace":
                        self._replace.Checked = True
                else:
                        self._append.Checked = True
	
	def InitializeComponent(self):
		self._gbSource = System.Windows.Forms.GroupBox()
		self._source = System.Windows.Forms.ComboBox()
		self._copy = System.Windows.Forms.RadioButton()
		self._move = System.Windows.Forms.RadioButton()
		self._destination = System.Windows.Forms.ComboBox()
		self._groupBox1 = System.Windows.Forms.GroupBox()
		self._label1 = System.Windows.Forms.Label()
		self._append = System.Windows.Forms.RadioButton()
		self._replace = System.Windows.Forms.RadioButton()
		self._seperator = System.Windows.Forms.TextBox()
		self._label2 = System.Windows.Forms.Label()
		self._label3 = System.Windows.Forms.Label()
		self._progress = System.Windows.Forms.ProgressBar()
		self._Okay = System.Windows.Forms.Button()
		self._Cancel = System.Windows.Forms.Button()
		self._UserText = System.Windows.Forms.TextBox()
		self._gbSource.SuspendLayout()
		self._groupBox1.SuspendLayout()
		self.worker = BackgroundWorker()
		self.SuspendLayout()
		#
		# Worker
		#
		self.worker.WorkerSupportsCancellation = True
		self.worker.WorkerReportsProgress = True
		self.worker.DoWork += self.DoWork
		self.worker.ProgressChanged += self.ReportProgress
		self.worker.RunWorkerCompleted += self.WorkerCompleted
		# 
		# gbSource
		# 
		self._gbSource.Controls.Add(self._move)
		self._gbSource.Controls.Add(self._copy)
		self._gbSource.Controls.Add(self._source)
		self._gbSource.Controls.Add(self._UserText)
		self._gbSource.Controls.Add(self._label3)
		self._gbSource.Location = System.Drawing.Point(12, 11)
		self._gbSource.Name = "gbSource"
		self._gbSource.Size = System.Drawing.Size(202, 97)
		self._gbSource.TabIndex = 0
		self._gbSource.TabStop = False
		self._gbSource.Text = "Source"
		# 
		# source
		# 
		self._source.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._source.FormattingEnabled = True
		self._source.Location = System.Drawing.Point(6, 19)
		self._source.Name = "source"
		self._source.Size = System.Drawing.Size(187, 21)
		self._source.TabIndex = 0
		self._source.Items.AddRange(System.Array[System.String]([
		"Added Time",
		"Age Rating",
		"Alternate Count",
		"Alternate Number",		
		"Alternate Series",
                "Book Age",
                "Book Collection Status",
                "Book Condition",
                "Book Location",
                "Book Notes",
                "Book Owner",
                "Book Price",
                "Book Store",
		"Characters",
		"Colorist",
		"Count",
		"Cover Artist",
		"Editor",
		"Format",
        "File Modified Time",
        "File Creation Time",
		"Genre",
		"Imprint",
		"Inker",
                "ISBN",
		"Letterer",
		"Locations",
                "Main Character Or Team",
		"Month",
		"Notes",
		"Number",
		"Penciller",
		"Published",
		"Publisher",
                "Review",
		"Scan Information",
		"Released Time",
		"Series",
                "Series Group",
                "Story Arc",
		"Summary",
		"Tags",
		"Teams",
		"Title",
		"User Text",
		"Volume",
		"Web",
		"Writer",
		"Year"
		]))
		self._source.SelectedIndex = 0
		self._source.SelectedIndexChanged += self.SouceIndexChanged
		# 
		# copy
		# 
		self._copy.Location = System.Drawing.Point(18, 42)
		self._copy.Name = "copy"
		self._copy.Size = System.Drawing.Size(55, 24)
		self._copy.TabIndex = 1
		self._copy.TabStop = True
		self._copy.Text = "Copy"
		self._copy.UseVisualStyleBackColor = True
		self._copy.Checked = True
		# 
		# move
		# 
		self._move.Location = System.Drawing.Point(125, 42)
		self._move.Name = "move"
		self._move.Size = System.Drawing.Size(60, 24)
		self._move.TabIndex = 2
		self._move.TabStop = True
		self._move.Text = "Move"
		self._move.UseVisualStyleBackColor = True
		#
		# User Text
		#
		self._label3.AutoSize = True
		self._label3.Location = System.Drawing.Point(2, 72)
		self._label3.Text = "User Text:"
		#
		# User Text
		#
		self._UserText.Size = Size(135, 20)
		self._UserText.Location = Point(60, 69)
		self._UserText.Enabled = False
		# 
		# destination
		# 
		self._destination.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList
		self._destination.FormattingEnabled = True
		self._destination.Location = System.Drawing.Point(6, 19)
		self._destination.Name = "destination"
		self._destination.Size = System.Drawing.Size(190, 21)
		self._destination.TabIndex = 1
		self._destination.Items.AddRange(System.Array[System.String]([
		"Added Time",
		"Age Rating",
		"Alternate Count",
		"Alternate Number",		
		"Alternate Series",
                "Book Age",
                "Book Collection Status",
                "Book Condition",
                "Book Location",
                "Book Notes",
                "Book Owner",
                "Book Price",
                "Book Store",
		"Characters",
		"Colorist",
		"Count",
		"Cover Artist",
		"Editor",
		"Format",
		"Genre",
		"Imprint",
		"Inker",
                "ISBN",
		"Letterer",
		"Locations",
                "Main Character Or Team",
		"Month",
		"Notes",
		"Number",
		"Penciller",
		"Published",
		"Publisher",
                "Review",
		"Scan Information",
		"Released Time",
		"Series",
                "Series Group",
                "Story Arc",
		"Summary",
		"Tags",
		"Teams",
		"Title",
		"Volume",
		"Web",
		"Writer",
		"Year"
		]))
		self._destination.SelectedIndex = 0
		# 
		# groupBox1
		# 
		self._groupBox1.Controls.Add(self._label2)
		self._groupBox1.Controls.Add(self._seperator)
		self._groupBox1.Controls.Add(self._replace)
		self._groupBox1.Controls.Add(self._append)
		self._groupBox1.Controls.Add(self._destination)
		self._groupBox1.Location = System.Drawing.Point(266, 11)
		self._groupBox1.Name = "groupBox1"
		self._groupBox1.Size = System.Drawing.Size(202, 97)
		self._groupBox1.TabIndex = 2
		self._groupBox1.TabStop = False
		self._groupBox1.Text = "Destination"
		# 
		# label1
		# 
		self._label1.AutoSize = True
		self._label1.Location = System.Drawing.Point(232, 53)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(16, 13)
		self._label1.TabIndex = 3
		self._label1.Text = "to"
		# 
		# append
		# 
		self._append.AutoSize = True
		self._append.Location = System.Drawing.Point(126, 46)
		self._append.Name = "append"
		self._append.Size = System.Drawing.Size(62, 17)
		self._append.TabIndex = 2
		self._append.TabStop = True
		self._append.Text = "Append"
		self._append.UseVisualStyleBackColor = True
		self._append.CheckedChanged += self.DestinationModeChanged
		# 
		# replace
		# 
		self._replace.AutoSize = True
		self._replace.Location = System.Drawing.Point(14, 46)
		self._replace.Name = "replace"
		self._replace.Size = System.Drawing.Size(65, 17)
		self._replace.TabIndex = 3
		self._replace.TabStop = True
		self._replace.Text = "Replace"
		self._replace.UseVisualStyleBackColor = True
		self._replace.Checked = True
		# 
		# seperator
		# 
		self._seperator.Location = System.Drawing.Point(154, 69)
		self._seperator.Name = "seperator"
		self._seperator.Size = System.Drawing.Size(42, 20)
		self._seperator.TabIndex = 4
		self._seperator.Enabled = False
		# 
		# label2
		# 
		self._label2.AutoSize = True
		self._label2.Location = System.Drawing.Point(92, 72)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(56, 13)
		self._label2.TabIndex = 5
		self._label2.Text = "Seperator:"
		# 
		# progressBar1
		# 
		self._progress.Location = System.Drawing.Point(12, 114)
		self._progress.Size = System.Drawing.Size(456, 17)
		self._progress.TabIndex = 4
		# 
		# Okay
		# 
		self._Okay.Location = System.Drawing.Point(312, 137)
		self._Okay.Name = "Okay"
		self._Okay.Size = System.Drawing.Size(75, 23)
		self._Okay.TabIndex = 5
		self._Okay.Text = "Start"
		self._Okay.UseVisualStyleBackColor = True
		self._Okay.Click += self.OkayClicked
		# 
		# Cancel
		# 
		self._Cancel.Location = System.Drawing.Point(393, 137)
		self._Cancel.Name = "Cancel"
		self._Cancel.Size = System.Drawing.Size(75, 23)
		self._Cancel.TabIndex = 6
		self._Cancel.Text = "Cancel"
		self._Cancel.UseVisualStyleBackColor = True
		self._Cancel.Click += self.CancelClicked
		# 
		# CopyFieldsForm
		# 
		self.ClientSize = System.Drawing.Size(483, 170)
		self.Controls.Add(self._Cancel)
		self.Controls.Add(self._Okay)
		self.Controls.Add(self._progress)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._groupBox1)
		self.Controls.Add(self._gbSource)
		self.Name = "CopyFieldsForm"
		self.Text = "Copy/Move Field"
		self.MinimizeBox = False
		self.MaximizeBox = False
		self.ShowIcon = True
		self.Icon = Icon(ICON)
		self.AcceptButton = self._Okay
		self.FormBorderStyle = FormBorderStyle.FixedDialog
		self.StartPosition = FormStartPosition.CenterParent
		self._gbSource.ResumeLayout(False)
		self._groupBox1.ResumeLayout(False)
		self._groupBox1.PerformLayout()
		self.ResumeLayout(False)
		self.PerformLayout()
		self.FormClosing += self.CheckClosing

	def SouceIndexChanged(self, sender, e):
		self._append.Enabled = True
		if sender.SelectedItem == "User Text":
			self._UserText.Enabled = True
			self._copy.Enabled = False
			self._move.Enabled = False

		else:
			self._UserText.Enabled = False
			self._copy.Enabled = True
			self._move.Enabled = True
			
			if sender.SelectedItem in ["Released Time", "Added Time"]:
				self._replace.Checked = True
				self._append.Enabled = False


	def CheckClosing(self, sender, e):
		if self.worker.IsBusy:
			self.worker.CancelAsync()
			e.Cancel = True

	def DestinationModeChanged(self, sender, e):
		self._seperator.Enabled = self._append.Checked

	def OkayClicked(self, sender, e):
		if self._Okay.Text == "Start":
			if self.worker.IsBusy == False:
				self.worker.RunWorkerAsync()

		else:
			self.DialogResult = DialogResult.OK

	def CancelClicked(self, sender, e):
		if self.worker.IsBusy:
			self.worker.CancelAsync()
		else:
			self.DialogResult = DialogResult.Cancel

	def DoWork(self, sender, e):
		if self._source.SelectedItem == "User Text":
			f, r = UserText(sender, self.books, self._UserText.Text, self._destination.SelectedItem.replace(" ", ""), self._append.Checked, self._seperator.Text)

		else:
			if self._move.Checked:
				f, r = MoveField(sender, self.books, self._source.SelectedItem.replace(" ", ""), self._destination.SelectedItem.replace(" ", ""), self._append.Checked, self._seperator.Text)
			else:
				f, r = CopyField(sender, self.books, self._source.SelectedItem.replace(" ", ""), self._destination.SelectedItem.replace(" ", ""), self._append.Checked, self._seperator.Text)

		e.Result = [f, r]

	def ReportProgress(self, sender, e):
		self.progresspercent = self.percentage*e.ProgressPercentage
		self._progress.Value = int(round(self.progresspercent))

	def WorkerCompleted(self, sender, e):
		self._Okay.Text = "Done"
		if e.Result[0] > 0:
			r = MessageBox.Show("Failed: %s" % (e.Result[0]) + "\n\nWould you like to see a report of the failed operations?", "Report", MessageBoxButtons.YesNo)
			if r == DialogResult.Yes:
				f = ReportForm(e.Result[1])
				f.ShowDialog()

def UserText(worker, books, text, destination, append, seperator):
	"""
	This function adds some user text to a destination field

	worker->The background worker with which to report progress
	books->The list or array of book objects
	text->The text to input
	destination->Name of the destination field as a string
	append->Bool of to append or not.
	spererator->Seperator text when appending (string)
	"""

	failed = 0
	count = 0
	report = System.Text.StringBuilder()
	for book in books:

		if worker.CancellationPending :
			return

		if append:
			orig = unicode(getattr(book, destination))
			orig += seperator + text
			try:
				setattr(book, destination, orig)
			except TypeError:
				try:
					setattr(book, destination, int(orig))
				except ValueError:
					failed += 1
					report.Append("Unable to add user text %s: %s to %s in book\n\n%s Vol.%s #%s" % (source, orig, destination, book.ShadowSeries, book.ShadowVolume, book.ShadowNumber))

		else:
			try:
				setattr(book, destination, text)
			except TypeError:
				try:
					setattr(book, destination, int(text))
				except ValueError:
					failed += 1
					report.Append("Unable to add user text %s: %s to %s in book\n\n%s Vol.%s #%s" % (source, unicode(getattr(book, readsource)), destination, book.ShadowSeries, book.ShadowVolume, book.ShadowNumber))

		count += 1
		worker.ReportProgress(count)
	return failed, report.ToString()


def CopyField(worker, books, source, destination, append, seperator):
	"""
	This function copies a source field to a destination field

	worker->The background worker with which to report progress
	books->The list or array of book objects
	source->Name of the field to copy as a string
	destination->Name of the destination field as a string
	append->Bool of to append or not.
	spererator->Seperator text when appending (string)
	"""

	#Since we want to read from the shadow values but they are read only make sure to keep a copy of the origianl source
	if source in ["Count", "Format", "Number", "Series", "Title", "Volume", "Year"]:
		readsource = "Shadow" + source
	else:
		readsource = source

	failed = 0
	count = 0
	report = System.Text.StringBuilder()
	for book in books:

		if worker.CancellationPending :
			return
		
		if source in ["ReleasedTime", "AddedTime", "Published", "FileModifiedTime", "FileCreationTime"]:
			d = getattr(book, source)
			try:
				if destination == "Published" :
					setattr(book, "Day", d.Day)
					setattr(book, "Month", d.Month)
					setattr(book, "Year", d.Year)

				elif destination in  ["Year", "Month", "Day"]:
					if destination == "Year" :
						value = d.Year
					if destination == "Month" :
						value = d.Month
					if destination == "Day" :
						value = d.Day
					setattr(book, destination, value)
				else : 
					setattr(book, destination, unicode(getattr(book, readsource)))
			except TypeError:
				try:
					setattr(book, destination, getattr(book, readsource))
				except:
					failed += 1
					report.Append("Unable to copy %s: %s to %s in book\n\n%s Vol.%s #%s" % (source, unicode(getattr(book, readsource)), destination, book.ShadowSeries, book.ShadowVolume, book.ShadowNumber))

		elif append:
			orig = unicode(getattr(book, destination))
			text = unicode(getattr(book, readsource))
			orig += seperator + text
			try:
				setattr(book, destination, orig)
			except TypeError:
				try:
					setattr(book, destination, int(orig))
				except ValueError:
					failed += 1
					report.Append("Unable to copy %s: %s to %s in book\n\n%s Vol.%s #%s" % (source, orig, destination, book.ShadowSeries, book.ShadowVolume, book.ShadowNumber))

		else:
			try:
				setattr(book, destination, unicode(getattr(book, readsource)))
			except TypeError:
				try:
					setattr(book, destination, int(getattr(book, readsource)))
				except:
					failed += 1
					report.Append("Unable to copy %s: %s to %s in book\n\n%s Vol.%s #%s" % (source, unicode(getattr(book, readsource)), destination, book.ShadowSeries, book.ShadowVolume, book.ShadowNumber))

		count += 1
		worker.ReportProgress(count)
	return failed, report.ToString()
			
def MoveField(worker, books, source, destination, append, seperator):
	"""
	This function moves a source field to a destination field

	worker->The background worker with which to report progress
	books->The list or array of book objects
	source->Name of the field to copy as a string
	destination->Name of the destination field as a string
	append->Bool of to append or not.
	spererator->Seperator text when appending (string)
	"""
	#Since we want to read from the shadow values but they are read only make sure to keep a copy of the origianl source
	if source in ["Count", "Format", "Number", "Series", "Title", "Volume", "Year"]:
		readsource = "Shadow" + source
	else:
		readsource = source
	empty = ""
	if source in ["Month", "Year", "Volume", "Count", "AlternateCount"]:
		empty = -1
	failed = 0
	count = 0
	report = System.Text.StringBuilder()
	for book in books:

		if worker.CancellationPending :
			return

		if source in ["ReleasedTime", "AddedTime", "Published"]:
			d = getattr(book, source)
			ed = System.DateTime(0001,1,1)
			try:
				if destination == "Published" :
					setattr(book, "Day", d.Day)
					setattr(book, "Month", d.Month)
					setattr(book, "Year", d.Year)

				elif destination in  ["Year", "Month", "Day"]:
					if destination == "Year" :
						value = d.Year
					if destination == "Month" :
						value = d.Month
					if destination == "Day" :
						value = d.Day
					setattr(book, destination, value)
				else : 
					setattr(book, destination, unicode(getattr(book, readsource)))
				setattr(book, source, ed)
			except TypeError:
				try:
					setattr(book, destination, getattr(book, readsource))
					if source == "Published" :
						setattr(book, "Day", -1)
						setattr(book, "Month", -1)
						setattr(book, "Year", -1)
					else:
						setattr(book, source, ed)
				except:
					failed += 1
					report.Append("Unable to copy %s: %s to %s in book\n\n%s Vol.%s #%s" % (source, unicode(getattr(book, readsource)), destination, book.ShadowSeries, book.ShadowVolume, book.ShadowNumber))

		elif append:
			orig = unicode(getattr(book, destination))
			text = unicode(getattr(book, readsource))
			orig += seperator + text
			try:
				setattr(book, destination, orig)
				setattr(book, source, empty)
			except TypeError:
				try:
					setattr(book, destination, int(orig))
					setattr(book, source, empty)
				except ValueError:
					failed += 1
					report.Append("Unable to move %s: %s to %s in book\n\n%s Vol.%s #%s" % (source, orig, destination, book.ShadowSeries, book.ShadowVolume, book.ShadowNumber))

			

		else:
			try:
				setattr(book, destination, unicode(getattr(book, readsource)))
				setattr(book, source, empty)
			except TypeError:
				try:
					setattr(book, destination, int(getattr(book, readsource)))
					setattr(book, source, empty)
				except:
					failed += 1
					report.Append("Unable to move %s: %s to %s in book\n\n%s Vol.%s #%s" % (source, unicode(getattr(book, readsource)), destination, book.ShadowSeries, book.ShadowVolume, book.ShadowNumber))

		count += 1
		worker.ReportProgress(count)
	return failed, report.ToString()


#Taken directly from my Library Organizer script with a couple tweaks.
class ReportForm(Form):
	def __init__(self, text):
		self.InitializeComponent()
		self._report.Text = text
	
	def InitializeComponent(self):
		self._button1 = System.Windows.Forms.Button()
		self._report = System.Windows.Forms.RichTextBox()
		self.SuspendLayout()
		# 
		# button1
		# 
		self._button1.Anchor = System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right
		self._button1.DialogResult = System.Windows.Forms.DialogResult.OK
		self._button1.Location = System.Drawing.Point(370, 399)
		self._button1.Name = "button1"
		self._button1.Size = System.Drawing.Size(75, 23)
		self._button1.TabIndex = 1
		self._button1.Text = "OK"
		self._button1.UseVisualStyleBackColor = True
		# 
		# report
		# 
		self._report.Anchor = System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right
		self._report.Location = System.Drawing.Point(12, 12)
		self._report.Name = "report"
		self._report.ReadOnly = True
		self._report.Size = System.Drawing.Size(425, 379)
		self._report.TabIndex = 4
		self._report.Text = ""
		self._report.BackColor = System.Drawing.Color.White
		# 
		# lomessagebox
		# 
		self.AcceptButton = self._button1
		self.ClientSize = System.Drawing.Size(453, 435)
		self.Controls.Add(self._report)
		self.Controls.Add(self._button1)
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Icon = Icon(ICON)
		self.ShowIcon = True
		self.Name = "ReportForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self.Text = "Report"
		self.ResumeLayout(False)
