#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Tuquito Control Center 0.2
 Copyright (C) 2010
 Author: Mario Colque <mario@tuquito.org.ar>
 Tuquito Team! - www.tuquito.org.ar

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; version 3 of the License.
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
"""

import gtk
import os
import commands
import gettext
import webkit
import string
from user import home

# i18n
gettext.install('tuquito-control-center', '/usr/share/tuquito/locale')

class MessageDialog:
    def __init__(self, title, message, style):
        self.title = title
        self.message = message
        self.style = style

    def show(self):
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, self.style, gtk.BUTTONS_OK)
        dialog.set_markup(_('<b>Error:</b>'))
        dialog.set_icon_name('preferences-desktop')
        dialog.format_secondary_markup(self.message)
        dialog.set_title(_('Control Center'))
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.run()
        dialog.destroy()

class ControlCenter():
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file('/usr/lib/tuquito/tuquito-control-center/control-center.glade')
        self.window = self.builder.get_object('window')
        self.builder.get_object('window').set_title(_('Control Center'))
        self.items_cache = []
        self.edit_handler_id = False
        self.add_handler_id = False

        # Define treeview
        self.treeview_items = self.builder.get_object('treeview_items')
        self.column1 = gtk.TreeViewColumn(_('Item'), gtk.CellRendererText(), text=0)
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

        self.builder.get_object('window').connect('destroy', gtk.main_quit)
        self.browser = webkit.WebView()
        self.builder.get_object('window').add(self.browser)
        self.browser.connect('button-press-event', lambda w, e: e.button == 3)
        text = {}
        text['appearance'] = _('Appearance')
        text['network'] = _('Network & Internet')
        text['programs'] = _('Programs')
        text['accounts'] = _('User Accounts')
        text['system'] = _('System and security')
        text['hard'] = _('Hardware and sound')
        text['about'] = _('About')
        text['back'] = _('Back to menu')

        text['change_theme'] = _('Change the background and theme')
        text['visual_efects'] = _('Configure visual effects')
        text['resolution'] = _('Adjust the screen resolution')
        text['screensaver'] = _('Set up screensaver')

        text['connections'] = _('Network connections')
        text['network_tools'] = _('Network tools')
        text['network_places'] = _('Network sites')
        text['proxy'] = _('Set up network proxy')
        text['firewall'] = _('Set up firewall')
        text['shared_files'] = _('Shared files and folders')

        text['add_programs'] = _('Add/Remove programs')
        text['favorites'] = _('Set favorite applications')
        text['trash'] = _('Remove unused files')

        text['user_accounts'] = _('User accounts and access control')
        text['add_users'] = _('Add or remove user accounts')
        text['control_parental'] = _('Set up Parental Control')
        text['gdm'] = _('Set up startup screen')

        text['hour'] = _('Set date and time')
        text['languages'] = _('Set up languages')
        text['boot'] = _('Set up startup')
        text['status'] = _('Status computer')
        text['backup'] = _('Make a backup')
        text['events'] = _('View system events')
        text['pass'] = _('Set passwords and encryption keys')

        text['info'] = _('System information')
        text['printer'] = _('View devices and printers')
        text['disks'] = _('Configure disks')
        text['drivers'] = _('Install drivers')
        text['wireless'] = _('Wireless network drivers')
        text['keyboard'] = _('Configure keyboard')
        text['mouse'] = _('Configure mouse')
        text['sound'] = _('Sound Preferences')
        text['bluetooth'] = _('Configure bluetooth')

        text['problems'] = _('Find and fix problems')
        text['edit_items'] = _('Edit items')

        template = open('/usr/lib/tuquito/tuquito-control-center/frontend/index.html').read()
        html = string.Template(template).safe_substitute(text)
        self.browser.load_html_string(html, 'file:/')
        self.browser.connect('title-changed', self.title_changed)
        self.window.show_all()

    def items_window(self, widget):
        self.model = gtk.TreeStore(str, str, str)
        self.model.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self.item_window = self.builder.get_object('items')
        self.item_window.set_title(_('Add or remove items'))
        self.builder.get_object('toolbutton_restore').set_label(_('Resore original'))
        items_file = open(self.category_file)
        for line in items_file:
            line = str.strip(line).split('|')
            title = line[0]
            command = line[1]
            try:
                owner = line[2]
            except:
                owner = False
            command_clean = command.split(' ')[0]
            if command_clean != 'gksu':
                command_search = command_clean
            else:
                 command_search = command.split(' ')[1]
            cmd = commands.getoutput('which ' + command_search)
            if cmd != '' or owner == 'user':
                iter = self.model.insert_before(None, None)
                self.model.set_value(iter, 0, _(title))
                self.model.set_value(iter, 1, command)
                self.model.set_value(iter, 2, title)
        self.treeview_items.set_model(self.model)
        del self.model
        self.builder.connect_signals(self)
        self.item_window.show()

    def add_item(self, widget):
        self.builder.get_object('title').set_text('')
        self.builder.get_object('code').set_text('')
        self.builder.get_object('add_item').set_title(_('Add item'))
        if self.edit_handler_id:
            self.builder.get_object('save').disconnect(self.edit_handler_id)
        if self.add_handler_id:
            self.builder.get_object('save').disconnect(self.add_handler_id)
        self.add_handler_id = self.builder.get_object('save').connect('clicked', self.save_item)
        self.builder.get_object('ltitle').set_label(_('Title: (eg Change Wallpaper)'))
        self.builder.get_object('lcode').set_label(_('Command app:'))
        self.builder.get_object('add_item').show()

    def close_add_item(self, widget, data=None):
        self.builder.get_object('add_item').hide()
        return True

    def close_items(self, widget, data=None):
        self.builder.get_object('items').hide()
        return True

    def save_item(self, widget):
        print "save_item"
        title = self.builder.get_object('title').get_text().strip()
        command = self.builder.get_object('code').get_text().strip()
        if not os.path.isfile(self.home_file):
            os.system('cp %s %s &' % (self.category_file, self.home_file))
            self.category_file = self.home_file
        if command != '' and title != '':
            item = title + '|' + command + '|user'
            exists = commands.getoutput('grep -wxs "%s" %s | wc -l' % (item, self.home_file))
            if exists != '0':
                message = MessageDialog('Error', _('The item <b>%s</b> already exists') % (title + '|' + command), gtk.MESSAGE_ERROR)
                message.show()
            else:
                self.model = self.treeview_items.get_model()
                iter = self.model.insert_before(None, None)
                self.model.set_value(iter, 0, title)
                self.model.set_value(iter, 1, command)
                os.system('echo "' + item + '" >>' + self.home_file)
                self.browser.execute_script("addItem('%s','%s','%s')" % (_(title), command, self.category))
                self.browser.execute_script("setContent('" + self.category + "')")
                self.items_cache.append(title)
                self.close_add_item(self)
                del self.model

    def remove_item(self, widget):
        selection = self.treeview_items.get_selection()
        (self.model, iter) = selection.get_selected()
        if not os.path.isfile(self.home_file):
            os.system('cp %s %s &' % (self.category_file,self.home_file))
            self.category_file = self.home_file
        if iter != None:
            title = self.model.get_value(iter, 0)
            command = self.model.get_value(iter, 1)
            item = title + '|' + command
            os.system("sed '/|user$/ d' " + self.home_file + ' > ' + self.home_file + '.back')
            os.system('mv ' + self.home_file + '.back ' + self.home_file)
            self.model.remove(iter)
            self.browser.execute_script("removeItem('" + command + "', '" + self.category + "')")

    def restore_items(self, widget):
        self.browser.execute_script("removeItem('all-items', '" + self.category + "')")
        os.system('cp %s %s' % (self.base_file,self.home_file))
        items_file = open(self.category_file)
        for line in items_file:
            if line != '':
                line = str.strip(line).split('|')
                title = line[0]
                command = line[1]
                try:
                    owner = line[2]
                except:
                    owner = False
                command_clean = command.split(' ')[0]
                if command_clean != 'gksu':
                    command_search = command_clean
                else:
                     command_search = command.split(' ')[1]
                cmd = commands.getoutput('which ' + command_search)
                if cmd != '' or owner == 'user':
                    self.browser.execute_script("addItem('%s','%s','%s')" % (_(title), command, self.category))
                    self.items_cache.append(title)
        self.browser.execute_script("setContent('" + self.category + "')")
        self.close_items(self)

    def edit_item(self, widget):
        selection = self.treeview_items.get_selection()
        (self.model, self.iter) = selection.get_selected()
        if self.iter != None:
            title = self.model.get_value(self.iter, 0)
            command = self.model.get_value(self.iter, 1)
            self.title_en = self.model.get_value(self.iter, 2)
            self.builder.get_object('title').set_text(title)
            self.builder.get_object('code').set_text(command)
            self.builder.get_object('add_item').set_title(_('Edit item'))
            if self.add_handler_id:
                self.builder.get_object('save').disconnect(self.add_handler_id)
            if self.edit_handler_id:
                self.builder.get_object('save').disconnect(self.edit_handler_id)
            self.edit_handler_id = self.builder.get_object('save').connect('clicked', self.save_edited_item)
            self.builder.get_object('ltitle').set_label(_('Title: (eg Change Wallpaper)'))
            self.builder.get_object('lcode').set_label(_('Command app:'))
            self.builder.get_object('add_item').show()
            self.old_item = self.title_en + '|' + command
            self.old_command = command

    def save_edited_item(self, widget):
        title = self.builder.get_object('title').get_text().strip()
        command = self.builder.get_object('code').get_text().strip()
        if not os.path.isfile(self.home_file):
            os.system('cp %s %s &' % (self.category_file,self.home_file))
            self.category_file = self.home_file
        if command != '' and title != '':
            new_item = title + '|' + command + '|user'
            self.model.set_value(self.iter, 0, title)
            self.model.set_value(self.iter, 1, command)
            self.model.set_value(self.iter, 2, title)
            os.system("sed 's/" + self.old_item.replace('/', '\/') + "/" + new_item.replace('/', '\/') + "/' " + self.home_file + ' > ' + self.home_file + '.back')
            os.system('mv ' + self.home_file + '.back ' + self.home_file)
            #usage: editItem('title','old_command', 'new_command')
            self.browser.execute_script("editItem('%s','%s', '%s')" % (_(title), self.old_command, command))
            self.browser.execute_script("setContent('" + self.category + "')")
            self.items_cache.append(title)
        self.close_add_item(self)
        del self.model

    def title_changed(self, view, frame, title):
        if title.startswith('exec:'):
            command = title.split(':')[1]
            cmd = commands.getoutput('which ' + command)
            if cmd != '':
                os.system('%s &' % command)
            else:
                message = MessageDialog('Error', _('The command <b>%s</b> is not found or not is executable') % command, gtk.MESSAGE_ERROR)
                message.show()
        elif title.startswith('category:'):
            self.category = title.split(':')[1]
            self.home_file = os.path.join(home, '.tuquito/tuquito-control-center/items/' + self.category)
            self.base_file = os.path.join('/usr/lib/tuquito/tuquito-control-center/items/', self.category)
            if os.path.isfile(self.home_file):
                self.category_file = self.home_file
            else:
                self.category_file = self.base_file
            #add items
            items_file = open(self.category_file)
            for line in items_file:
                line = str.strip(line).split('|')
                title = line[0]
                command = line[1]
                try:
                    owner = line[2]
                except:
                    owner = False
                command_clean = command.split(' ')[0]
                if command_clean != 'gksu':
                    command_search = command_clean
                else:
                     command_search = command.split(' ')[1]
                cmd = commands.getoutput('which ' + command_search)
                if cmd != '' or owner == 'user':
                    if title not in self.items_cache:
                        self.items_cache.append(title)
                        #usage: addItem(title, command, category)
                        self.browser.execute_script("addItem('" + _(title) + "','" + command + "','" + self.category + "')")
        elif title == 'add-item':
            self.items_window(self)
        elif title == 'about':
            os.system('/usr/lib/tuquito/tuquito-control-center/about.py &')

if __name__ == '__main__':
    category_list = ['accounts', 'appearance', 'hardware', 'network', 'programs', 'system']
    home_path = os.path.join(home, '.tuquito/tuquito-control-center/items')
    if not os.path.exists(home_path):
        os.system('mkdir -p ' + home_path)
    gtk.gdk.threads_init()
    ControlCenter()
    gtk.main()
