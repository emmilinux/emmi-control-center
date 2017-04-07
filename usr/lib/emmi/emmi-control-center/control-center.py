#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Tuquito Control Center
 Copyright (C) 2010
 Author: Mario Colque <mario@emmi.org.ar>
 Tuquito Team! - www.emmi.org.ar

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
import webkit
import string
import json
from user import home

# i18n
gettext.install('emmi-control-center', '/usr/share/emmi/locale')

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
        self.builder.add_from_file('/usr/lib/emmi/emmi-control-center/control-center.glade')
        self.window = self.builder.get_object('window')
        self.builder.get_object('window').set_title(_('Control Center'))
        self.edit_handler_id = False
        self.add_handler_id = False
        self.items_cache = []
        self.items_advanced_cache = []
        self.theme = gtk.icon_theme_get_default()
        self.read_preferences(self)

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

        self.text = {}
        self.set_options_status()
        self.text['appearance'] = _('Appearance')
        self.text['network'] = _('Network & Internet')
        self.text['programs'] = _('Programs')
        self.text['user_accounts'] = _('User accounts and access control')
        self.text['accounts'] = _('User Accounts')
        self.text['system'] = _('System and security')
        self.text['hard'] = _('Hardware and sound')
        self.text['about'] = _('About')
        self.text['back'] = _('Back to menu')

        self.text['options'] = _('Options')
        self.text['mode'] = _('Mode')
        self.text['advanced_mode'] = _('Advanced mode')
        self.text['normal_mode'] = _('Normal mode')
        self.text['suggestions'] = _('Suggestions')
        self.text['show_suggestions'] = _('Show suggestions')
        self.text['visual'] = _('Visual effects')
        self.text['nice'] = _('Use visual effects (slower)')
        self.text['note_visual'] = _('If you want better performance (faster), disable visual effects.')
        self.text['apply'] = _('Apply')
        self.text['has_suggestions'] = 'hidden'

        self.text['change_theme'] = _('Change the background and theme')
        self.text['visual_efects'] = _('Configure visual effects')
        self.text['resolution'] = _('Adjust the screen resolution')

        self.text['connections'] = _('Network connections')
        self.text['network_tools'] = _('Network tools')
        self.text['network_places'] = _('Network sites')

        self.text['add_users'] = _('Add or remove user accounts')
        self.text['control_parental'] = _('Set up Parental Control')

        self.text['drivers'] = _('Install drivers')
        self.text['printer'] = _('View devices and printers')

        self.text['status'] = _('Status computer')
        self.text['backup'] = _('Make a backup')

        self.text['add_programs'] = _('Add/Remove programs')
        self.text['favorites'] = _('Set favorite applications')
        self.text['trash'] = _('Remove unused files')
        self.text['problems'] = _('Find and fix problems')

        self.text['edit_items'] = _('Edit items')
        self.text['suggestions'] = _('Suggested programs')

        if not self.mode:
            self.load_advanced()

        template = self.get_template()
        html = string.Template(template.read()).safe_substitute(self.text)
        template.close()
        self.browser.load_html_string(html, 'file:/')
        self.browser.connect('title-changed', self.title_changed)
        self.window.show_all()

    def set_options_status(self):
        if self.mode:
            self.text['input_mode_id'] = 'checked="checked"'
            self.text['input_mode'] = ''
        else:
            self.text['input_mode_id'] = ''
            self.text['input_mode'] = 'checked="checked"'
        if self.show_suggestions:
            self.text['input_suggestions'] = 'checked="checked"'
        else:
            self.text['input_suggestions'] = ''
        if self.visual_effects:
            self.text['input_visual'] = 'checked="checked"'
        else:
            self.text['input_visual'] = ''

    def get_template(self):
        if self.visual_effects and self.mode:
            template = open('/usr/lib/emmi/emmi-control-center/frontend/default.html')
        elif not self.visual_effects and self.mode:
            template = open('/usr/lib/emmi/emmi-control-center/frontend/default-faster.html')
        elif self.visual_effects and not self.mode:
            template = open('/usr/lib/emmi/emmi-control-center/frontend/advanced.html')
        else:
            template = open('/usr/lib/emmi/emmi-control-center/frontend/advanced-faster.html')
        return template

    def change_skin(self, widget):
        self.set_options_status()
        self.items_cache = []
        template = self.get_template()
        if not self.mode:
            self.load_advanced()
        html = string.Template(template.read()).safe_substitute(self.text)
        template.close()
        self.browser.load_html_string(html, 'file:/')

    def read_preferences(self, widget):
        self.pref_file = os.path.join(home, '.emmi/emmi-control-center/preferences')
        if os.path.isfile(self.pref_file):
            pref_file = open(self.pref_file)
            dic = json.load(pref_file)
            pref_file.close()
            self.mode = bool(dic['mode'])
            self.show_suggestions = bool(dic['show_suggestions'])
            self.visual_effects = bool(dic['visual_effects'])
        else:
            self.mode = True
            self.show_suggestions = True
            self.visual_effects = True

    def save_preferences(self, widget):
        if self.show_suggestions == "true":
            self.show_suggestions = True
        else:
            self.show_suggestions = False
        if self.mode == "true":
            self.mode = True
        else:
            self.mode = False
        if self.visual_effects == "true":
            self.visual_effects = True
        else:
            self.visual_effects = False
        dic = dict([("show_suggestions", self.show_suggestions), ("mode", self.mode), ("visual_effects", self.visual_effects)])
        pref_file = open(self.pref_file, 'w')
        json.dump(dic, pref_file)
        pref_file.close()

    def items_window(self, widget):
        self.model = gtk.TreeStore(str, str, str)
        self.model.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self.item_window = self.builder.get_object('items')
        self.item_window.set_title(_('Add or remove items'))
        self.builder.get_object('toolbutton_restore').set_label(_('Resore original'))
        items_file = open(self.category_file)
        dic = json.load(items_file)
        items_file.close()
        for k, v in dic.iteritems():
            command = k
            title = v['title']
            owner = v['owner']
            icon = v['icon']
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
                self.model.set_value(iter, 2, icon)
        self.treeview_items.set_model(self.model)
        del self.model
        self.builder.connect_signals(self)
        self.item_window.show()

    def add_item(self, widget):
        self.builder.get_object('title').set_text('')
        self.builder.get_object('code').set_text('')
        self.builder.get_object('icon').set_text('applications-other')
        self.builder.get_object('add_item').set_title(_('Add item'))
        if self.edit_handler_id:
            self.builder.get_object('save').disconnect(self.edit_handler_id)
        if self.add_handler_id:
            self.builder.get_object('save').disconnect(self.add_handler_id)
        self.add_handler_id = self.builder.get_object('save').connect('clicked', self.save_item)
        self.builder.get_object('ltitle').set_label(_('Title: (eg Change Wallpaper)'))
        self.builder.get_object('lcode').set_label(_('Command app:'))
        self.builder.get_object('licon').set_label(_('Icon file:'))
        self.builder.get_object('lexpander').set_label(_('Options icon'))
        self.builder.get_object('add_item').show()

    def close_add_item(self, widget, data=None):
        self.builder.get_object('add_item').hide()
        return True

    def close_items(self, widget, data=None):
        self.builder.get_object('items').hide()
        return True

    def save_item(self, widget):
        title = self.builder.get_object('title').get_text().strip()
        command = self.builder.get_object('code').get_text().strip()
        icon = self.builder.get_object('icon').get_text().strip()
        no_exists = True
        if not os.path.isfile(self.home_file):
            os.system('cp %s %s' % (self.category_file, self.home_file))
            self.category_file = self.home_file
        if command != '' and title != '':
            items_file = open(self.category_file)
            dic = json.load(items_file)
            items_file.close()
            for k, v in dic.iteritems():
                if k == command:
                    no_exists = False
                    message = MessageDialog('Error', _('The command <b>%s</b> already exists') % command, gtk.MESSAGE_ERROR)
                    message.show()
                if dic[k]['title'] == title:
                    no_exists = False
                    message = MessageDialog('Error', _('The title <b>%s</b> already exists') % title, gtk.MESSAGE_ERROR)
                    message.show()
            if no_exists:
                if not os.path.isfile(icon):
                    if self.theme.has_icon(icon):
                        iconInfo = self.theme.lookup_icon(icon, 24, 0)
                    else:
                        iconInfo = self.theme.lookup_icon("applications-other", 24, 0)
                    icon = iconInfo.get_filename()
                dic[command] = dict([('title', title), ('owner', 'user'), ('icon', icon)])
                self.model = self.treeview_items.get_model()
                iter = self.model.insert_before(None, None)
                self.model.set_value(iter, 0, title)
                self.model.set_value(iter, 1, command)
                items_file = open(self.category_file, 'w')
                json.dump(dic, items_file)
                items_file.close()
                self.browser.execute_script("addItem('%s','%s','%s','%s')" % (_(title), command, self.category, icon))
                self.browser.execute_script("setContent('" + self.category + "')")
                self.items_cache.append(command)
                self.close_add_item(self)
                del self.model

    def remove_item(self, widget):
        selection = self.treeview_items.get_selection()
        (self.model, iter) = selection.get_selected()
        if not os.path.isfile(self.home_file):
            os.system('cp %s %s' % (self.category_file,self.home_file))
            self.category_file = self.home_file
        if iter != None:
            command = self.model.get_value(iter, 1)
            items_file = open(self.category_file)
            dic = json.load(items_file)
            items_file.close()
            dic.pop(command)
            items_file = open(self.category_file, 'w')
            json.dump(dic, items_file)
            items_file.close()
            self.model.remove(iter)
            self.browser.execute_script("removeItem('" + command + "', '" + self.category + "')")
            self.items_cache.remove(command)

    def restore_items(self, widget):
        self.browser.execute_script("removeItem('all-items', '" + self.category + "')")
        os.system('cp %s %s' % (self.base_file, self.home_file))
        items_file = open(self.category_file)
        dic = json.load(items_file)
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
            if cmd != '':
                if not os.path.isfile(icon):
                    if self.theme.has_icon(icon):
                        iconInfo = self.theme.lookup_icon(icon, 24, 0)
                    else:
                        iconInfo = self.theme.lookup_icon("applications-other", 24, 0)
                    icon = iconInfo.get_filename()
                self.browser.execute_script("addItem('%s','%s','%s','%s')" % (_(title), command, self.category, icon))
                if command not in self.items_cache:
                    self.items_cache.append(command)
        items_file.close()
        self.browser.execute_script("setContent('" + self.category + "')")
        self.close_items(self)

    def edit_item(self, widget):
        selection = self.treeview_items.get_selection()
        (self.model, self.iter) = selection.get_selected()
        if self.iter != None:
            title = self.model.get_value(self.iter, 0)
            command = self.model.get_value(self.iter, 1)
            icon = self.model.get_value(self.iter, 2)
            self.builder.get_object('title').set_text(title)
            self.builder.get_object('code').set_text(command)
            self.builder.get_object('icon').set_text(icon)
            self.builder.get_object('add_item').set_title(_('Edit item'))
            if self.add_handler_id:
                self.builder.get_object('save').disconnect(self.add_handler_id)
            if self.edit_handler_id:
                self.builder.get_object('save').disconnect(self.edit_handler_id)
            self.edit_handler_id = self.builder.get_object('save').connect('clicked', self.save_edited_item)
            self.builder.get_object('ltitle').set_label(_('Title: (eg Change Wallpaper)'))
            self.builder.get_object('lcode').set_label(_('Command app:'))
            self.builder.get_object('licon').set_label(_('Icon file:'))
            self.builder.get_object('lexpander').set_label(_('Options icon'))
            self.builder.get_object('add_item').show()
            self.old_command = command

    def save_edited_item(self, widget):
        title = self.builder.get_object('title').get_text().strip()
        command = self.builder.get_object('code').get_text().strip()
        icon = self.builder.get_object('icon').get_text().strip()
        if not os.path.isfile(self.home_file):
            os.system('cp %s %s' % (self.category_file,self.home_file))
            self.category_file = self.home_file
        if command != '' and title != '':
            if not os.path.isfile(icon):
                if self.theme.has_icon(icon):
                    iconInfo = self.theme.lookup_icon(icon, 24, 0)
                else:
                    iconInfo = self.theme.lookup_icon("applications-other", 24, 0)
                icon = iconInfo.get_filename()
            items_file = open(self.category_file)
            dic = json.load(items_file)
            items_file.close()
            items_file = open(self.category_file, 'w')
            dic.pop(self.old_command)
            dic[command] = dict([('title', title), ('owner', 'user'), ('icon', icon)])
            self.model.set_value(self.iter, 0, title)
            self.model.set_value(self.iter, 1, command)
            self.model.set_value(self.iter, 2, icon)
            items_file = open(self.category_file, 'w')
            json.dump(dic, items_file)
            items_file.close()
            #usage: editItem('title','old_command', 'new_command', 'icon')
            self.browser.execute_script("editItem('%s', '%s', '%s', '%s')" % (_(title), self.old_command, command, icon))
            self.browser.execute_script("setContent('" + self.category + "')")
            if command not in self.items_cache:
                self.items_cache.append(command)
        self.close_add_item(self)
        del self.model

    def search_icon(self, widget):
        self.builder.get_object('filechooserdialog').set_title(_('Control Center'))
        self.builder.get_object('filechooserdialog').set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        self.builder.get_object('filechooserdialog').show()

    def on_search_ok(self, widget, data=None):
        icon_file = self.builder.get_object('filechooserdialog').get_filename().strip()
        if icon_file != '':
            self.builder.get_object('icon').set_text(icon_file)
        else:
            print 'No hay icono seleccionado'
        self.search_close(self)

    def search_close(self, widget, data=None):
        self.builder.get_object('filechooserdialog').hide()
        return True

    def about(self, widget):
        abt = self.builder.get_object('about')
        abt.connect('response', self.close_about)
        abt.connect('delete-event', self.close_about)
        abt.connect('destroy-event', self.close_about)
        abt.set_name(_('Control Center'))
        abt.set_comments(_('Configuration tool for Tuquito'))
        abt.show()

    def close_about(self, widget, data=None):
        widget.hide()
        return True

    def load_advanced(self):
        li_content = []
        self.category = 'advanced'
        self.home_file = os.path.join(home, '.emmi/emmi-control-center/items/' + self.category)
        self.base_file = os.path.join('/usr/lib/emmi/emmi-control-center/items/', self.category)
        self.has_suggestions = False
        if os.path.isfile(self.home_file):
            self.category_file = self.home_file
        else:
            self.category_file = self.base_file
        items_file = open(self.category_file)
        dic = json.load(items_file)
        items_file.close()
        for k, v in dic.iteritems():
            command = k
            title = v['title']
            owner = v['owner']
            icon = v['icon']
            if not os.path.isfile(icon):
                if self.theme.has_icon(icon):
                    iconInfo = self.theme.lookup_icon(icon, 24, 0)
                    icon = iconInfo.get_filename()
                else:
                    iconInfo = self.theme.lookup_icon("applications-other", 24, 0)
                    if iconInfo and os.path.exists(iconInfo.get_filename()):
                        icon = iconInfo.get_filename()
                    else:
                        icon = '/usr/lib/emmi/emmi-control-center/frontend/images/applications-other.png'
            command_clean = command.split(' ')[0]
            if command_clean != 'gksu':
                command_search = command_clean
            else:
                 command_search = command.split(' ')[1]
            cmd = commands.getoutput('which ' + command_search)
            if cmd == '' and not self.has_suggestions and self.show_suggestions:
                self.has_suggestions = True
                self.text['has_suggestions'] = ''
            if cmd != '' or owner == 'user':
                content = "<li id='" + command + "' onclick='javascript:changeTitle(\"exec:" + command + "\")' class='item' style='background-image: url(" + icon + ")'>" + _(title) + "</li>"
                li_content.append(content)
                self.items_cache.append(command)
        self.text['li_content'] = '\n'.join(li_content)

    def title_changed(self, view, frame, title):
        self.current_commands = []
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
            self.home_file = os.path.join(home, '.emmi/emmi-control-center/items/' + self.category)
            self.base_file = os.path.join('/usr/lib/emmi/emmi-control-center/items/', self.category)
            if os.path.isfile(self.home_file):
                self.category_file = self.home_file
            else:
                self.category_file = self.base_file
            items_file = open(self.category_file)
            dic = json.load(items_file)
            items_file.close()
            for k, v in dic.iteritems():
                self.current_commands.append(k)
                command = k
                title = v['title']
                owner = v['owner']
                icon = v['icon']
                if not os.path.isfile(icon):
                    if self.theme.has_icon(icon):
                        iconInfo = self.theme.lookup_icon(icon, 24, 0)
                        icon = iconInfo.get_filename()
                    else:
                        iconInfo = self.theme.lookup_icon("applications-other", 24, 0)
                        if iconInfo and os.path.exists(iconInfo.get_filename()):
                            icon = iconInfo.get_filename()
                        else:
                            icon = '/usr/lib/emmi/emmi-control-center/frontend/images/applications-other.png'
                command_clean = command.split(' ')[0]
                if command_clean != 'gksu':
                    command_search = command_clean
                else:
                     command_search = command.split(' ')[1]
                cmd = commands.getoutput('which ' + command_search)
                if cmd != '' or owner == 'user':
                    if command not in self.items_cache:
                        self.items_cache.append(command)
                        #usage: addItem(title, command, category, icon)
                        self.browser.execute_script("addItem('%s','%s','%s','%s')" % (_(title), command, self.category, icon))
                if cmd == '' and self.show_suggestions:
                    self.browser.execute_script("setSuggestions('" + self.category + "', 'show')")
            self.browser.execute_script("setContent('" + self.category + "')")
        elif title == 'edit-item':
            self.items_window(self)
        elif title == 'suggestions':
            os.system('/usr/lib/emmi/emmi-control-center/suggestions.py %s &' % self.category)
        elif title == 'about':
            self.about(self)
        #usage: save-options:mode:show_suggestions:visual_effects
        elif title.startswith('save-options:'):
            self.mode = title.split(':')[1]
            self.show_suggestions = title.split(':')[2]
            self.visual_effects = title.split(':')[3]
            self.save_preferences(self)
            for i in self.current_commands:
                if i in self.items_cache:
                    self.items_cache.remove(i)
            self.change_skin(self)

if __name__ == '__main__':
    home_path = os.path.join(home, '.emmi/emmi-control-center/items')
    if not os.path.exists(home_path):
        os.system('mkdir -p ' + home_path)
    gtk.gdk.threads_init()
    ControlCenter()
    gtk.main()
