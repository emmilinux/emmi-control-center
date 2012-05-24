#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Tuquito Control Center
 Copyright (C) 2010
 Author: Mario Colque <mario@tuquito.org.ar>
 Tuquito Team! - www.tuquito.org.ar

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; version 3 of the License.
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
"""

import gtk
import gettext
import os
import commands
import apt
import sys
import json
import tempfile
from subprocess import Popen, PIPE

# i18n
gettext.install('tuquito-control-center', '/usr/share/tuquito/locale')

class MessageDialog:
    def __init__(self, message, style):
        self.message = message
        self.style = style

    def show(self):
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, self.style, gtk.BUTTONS_OK)
        dialog.set_markup(_('<b>Information:</b>'))
        dialog.set_icon_name('preferences-desktop')
        dialog.format_secondary_markup(self.message)
        dialog.set_title(_('Control Center'))
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.run()
        dialog.destroy()

class Suggestions:
    def __init__(self):
        self.glade = gtk.Builder()
        self.glade.add_from_file('/usr/lib/tuquito/tuquito-control-center/suggestions.glade')
        self.window = self.glade.get_object('suggestions')
        self.window.set_title(_('Control Center'))
        self.treeview_items = self.glade.get_object('treeview_items')
        self.column1 = gtk.TreeViewColumn(_('App'), gtk.CellRendererText(), text=0)
        self.column1.set_sort_column_id(0)
        self.column1.set_resizable(True)
        self.column2 = gtk.TreeViewColumn(_('Command'), gtk.CellRendererText(), text=1)
        self.column2.set_sort_column_id(1)
        self.column2.set_resizable(True)
        self.treeview_items.append_column(self.column1)
        self.treeview_items.append_column(self.column2)
        self.treeview_items.set_headers_clickable(True)
        self.treeview_items.set_reorderable(False)
        self.treeview_items.show()

        self.cache = apt.Cache()
        self.suggestions = []
        self.category_file = os.path.join('/usr/lib/tuquito/tuquito-control-center/items',category)

        self.model = gtk.TreeStore(str, str)
        self.model.set_sort_column_id(0, gtk.SORT_ASCENDING)
        items_file = open(self.category_file)
        dic = json.load(items_file)
        items_file.close()
        for k, v in dic.iteritems():
            command = k
            title = v['title']
            icon = v['icon']
            command_clean = command.split(' ')[0]
            if command_clean != 'gksu':
                command_search = command_clean
            else:
                 command_search = command.split(' ')[1]
            cmd = commands.getoutput('which ' + command_search)
            if cmd == '' and (command_search in self.cache):
                iter = self.model.insert_before(None, None)
                self.model.set_value(iter, 0, _(title))
                self.model.set_value(iter, 1, command_search)
                self.suggestions.append(command)
        self.treeview_items.set_model(self.model)
        del self.model
        self.glade.connect_signals(self)
        self.window.show()

    def info_item(self, widget):
        selection = self.treeview_items.get_selection()
        (self.model, iter) = selection.get_selected()
        if iter != None:
            command = self.model.get_value(iter, 1)
            description = self.cache[command].versions[0].description
            size = convert(self.cache[command].versions[0].size)
            version = self.cache[command].versions[0].version
            text_pack = _('<b>Package</b>: %s') % command
            text_desc = _('\n<b>Description</b>:\n%s') % description
            text_ver = _('\n<b>Version</b>: %s') % version
            text_size = _('\n<b>Size</b>: %s') % size
            text = text_pack + text_desc + text_ver + text_size
            message = MessageDialog(text, gtk.MESSAGE_INFO)
            message.show()

    def install(self, widget):
        selection = self.treeview_items.get_selection()
        (self.model, iter) = selection.get_selected()
        if iter != None:
            command = self.model.get_value(iter, 1)
            self.window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            self.window.set_sensitive(False)
            cmd = ['gksu', '\'/usr/sbin/synaptic', '--hide-main-window', '--non-interactive']
            f = tempfile.NamedTemporaryFile()
            f.write('%s\tinstall\n' % command)
            cmd.append('--set-selections-file')
            cmd.append('%s\'' % f.name)
            cmd.append('-D /usr/share/applications/synaptic.desktop')
            f.flush()
            comnd = Popen(' '.join(cmd), shell=True)
            returnCode = comnd.wait()
            self.window.window.set_cursor(None)
            self.window.set_sensitive(True)
            self.model.remove(iter)

    def close_info(self, widget):
        self.dialog.hide()
        return True

    def quit(self, widget, data=None):
        gtk.main_quit()
        return True

def convert(size):
    strSize = str(size) + _('B')
    if (size >= 1000):
        strSize = str(size / 1000) + _('KB')
    if (size >= 1000000):
        strSize = str(size / 1000000) + _('MB')
    if (size >= 1000000000):
        strSize = str(size / 1000000000) + _('GB')
    return strSize

if __name__ == '__main__':
    try:
        category = sys.argv[1]
        win = Suggestions()
        gtk.main()
    except Exception, e:
        print e
        sys.exit(1)
