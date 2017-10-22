#!/usr/bin/env python3

import io, subprocess, os
from gi.repository import Gtk

def entry_activated(sEntry):
	global found
	print(sEntry.get_text())
	
	# when user searches for dependency, locate within centraltextV and highlight found dependency
	search_str = sEntry.get_text()
	start_iter = buffer1.get_start_iter()
	found = start_iter.forward_search(search_str, 0, None) # search for search_str, beginning with the start of the buffer
	if found: # if found = True
		match_start, match_end = found # declare both with the same value
		buffer1.select_range(match_start, match_end) # highlight the found value
		
	sL = buffer1.get_line(found) # get line of found dependency -> 0 = 1st line
	buffer2.set_text(dpkg_array[sL]) # move found dependency to buffer of side_textV

def remove_dependency(self):
		for line in side_textV:
			subprocess.call("gksudo dpkg --force-all -P %d" & line, shell=True)

class dpkgApp(Gtk.Window):
	def __init__(self):
		
		Gtk.Window.__init__(self, title="Software/dependencies")
		self.set_default_size(800, 500)
		
		fixed = Gtk.Fixed()
		self.add(fixed)
		
		# search widgets and search button
		sEntry = Gtk.Entry()
		sEntry.set_placeholder_text("Search for a dependency")
		sEntry.connect("activate", entry_activated)
		sEntry.set_size_request(665, 10)
		fixed.put(sEntry, 5, 5)
		
		# search button
		self.applyBtn = Gtk.Button("REMOVE ALL");
		self.applyBtn.connect("clicked", remove_dependency)
		self.applyBtn.set_size_request(120, 10)
		fixed.put(self.applyBtn, 675, 5)
		
		# central text view - contains output of "dpkg --get-selections"
		self.central_scroll = Gtk.ScrolledWindow()
		self.central_scroll.set_size_request(660, 420)
		fixed.put(self.central_scroll, 5, 50)
		
		central_textV = Gtk.TextView()
		self.central_scroll.add(central_textV)
		
		# side text view - contains dependencies to be removed
		side_scroll = Gtk.ScrolledWindow()
		side_scroll.set_size_request(120, 420)
		fixed.put(side_scroll, 675, 50)
		
		global side_textV
		side_textV = Gtk.TextView()
		side_scroll.add(side_textV)
		
		global  buffer2
		buffer2 = Gtk.TextBuffer()
		side_textV.set_buffer(buffer2)
		
		label = Gtk.Label("Software/Dependencies visible can be found in the file \"home/.dpkg_config/dpkg-selections\"")
		fixed.put(label, 20, 478)
		
		# ------------------------------------------------------------------------------
		# ------------------------------------------------------------------------------
		
		# create /.dpkg_config/ directory and add "dpkg-selections" file
		global HOME, DPKG_FILE, buffer1
		HOME = os.environ["HOME"]
		DPKG_FILE = HOME+"/.dpkg_config/"
		subprocess.call("mkdir "+HOME+"/.dpkg_config && touch "+DPKG_FILE+"dpkg-selections", shell=True)
		
		# remove all instances of the string "install" from "dkg-selections" file
		wR = open(DPKG_FILE+"dpkg-selections", "w")
		rE = open(DPKG_FILE+"dpkg-selections", "r")
		for line in rE:
			wR.write(line.replace("install", " "))
		
		# execute "dpkg --get-selections" and add the output to dpkg_output
		dpkg_output = os.popen("dpkg --get-selections")
		
		with open(DPKG_FILE+"dpkg-selections", "w") as w:
			w.writelines(dpkg_output)
			for lines in central_textV:
				w.write(line.replace("install", ""))
			w.close()
			
		with open(DPKG_FILE+"dpkg-selections", "r") as r:
			dpkgOUT = r.read()
			r.close()
			
		buffer1 = Gtk.TextBuffer()
		central_textV.set_buffer(buffer1)
		buffer1.set_text(dpkgOUT)
		central_textV.set_editable(False)
		central_textV.set_wrap_mode(True)
		central_textV.set_cursor_visible(False)
			
		self.create_dpkgArray()
	
	# append each line from "dpkg-selections" file as a string to dpkg_array[]
	def create_dpkgArray(self):
		global dpkg_array
		with open(DPKG_FILE+"dpkg-selections","r") as r:
			dpkg_array = r.readlines()



window = dpkgApp()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
