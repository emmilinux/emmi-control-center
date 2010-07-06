#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Tuquito Control Center 0.1
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

import gtk, pygtk
pygtk.require("2.0")
import commands, os
import gettext, webkit, string
from user import home

# i18n
gettext.install('tuquito-control-center', '/usr/share/tuquito/locale')

class Center():
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file('/usr/lib/tuquito/tuquito-control-center/control-center.glade')
		self.window = self.builder.get_object('window')
		self.builder.get_object('window').set_title(_('Control Center'))

		user = os.getenv('USER')

		self.builder.get_object('window').connect('destroy', gtk.main_quit)
		browser = webkit.WebView()
		self.builder.get_object('scrolled').add(browser)
		browser.connect('button-press-event', lambda w, e: e.button == 3)
		text = {}
		text['appearance'] = _('Appearance')
		text['network'] = _('Network & Internet')
		text['programs'] = _('Programs')
		text['accounts'] = _('User Accounts')
		text['system'] = _('System and security')
		text['hard'] = _('Hardware and sound')
		text['about'] = _('About')
		text['back'] = _('Back to menu')

		text['cambiar_tema'] = _('Change the background and theme') 
		text['efectos_visuales'] = _('Configure visual effects')
		text['resolucion'] = _('Adjust the screen resolution')

		text['conexiones'] = _('Network connections')
		text['herramientas_red'] = _('Network tools')
		text['sitios_red'] = _('Network sites')

		text['agregar_prog'] = _('Add/Remove programs')
		text['favoritas'] = _('Set favorite applications')
		text['arch_sin_uso'] = _('Remove unused files')

		text['cuentas_control'] = _('User accounts and access control')
		text['agregar_usuarios'] = _('Add or remove user accounts')
		text['control_parental'] = _('Set up Parental Control')

		text['estado_equipo'] = _('Status computer')
		text['backup'] = _('Make a backup')
		text['corregir_problemas'] = _('Find and fix problems')

		text['impresoras'] = _('View devices and printers')
		text['drivers'] = _('Install drivers')

		text['salvapantallas'] = _('Set up screensaver')

		text['proxy'] = _('Set up network proxy')
		text['firewall'] = _('Set up firewall')
		text['arch_comp'] = _('Shared files and folders')

		text['gdm'] = _('Set up startup screen')

		text['hora'] = _('Set date and time')
		text['idiomas'] = _('Set up languages')
		text['inicio'] = _('Set up startup')
		text['sucesos'] = _('View system events')
		text['pass'] = _('Set passwords and encryption keys')

		text['info'] = _('System information')
		text['discos'] = _('Configure disks')
		text['inalambricas'] = _('Wireless network drivers')
		text['teclado'] = _('Configure keyboard')
		text['mouse'] = _('Configure mouse')
		text['sonido'] = _('Sound Preferences')
		text['bluetooth'] = _('Configure bluetooth')
		
		template = open('/usr/lib/tuquito/tuquito-control-center/frontend/index.html').read()		
		html = string.Template(template).safe_substitute(text)
		browser.load_html_string(html, 'file:/')
		browser.connect('title-changed', self.title_changed)
		self.window.show_all()

	def title_changed(self, view, frame, title):
		if title == 'tema_fondo':
				os.system('gnome-appearance-properties &')
		elif title == 'compiz':
			os.system('simple-ccsm &')
		elif title == 'monitores':
			os.system('gnome-display-properties &')
		elif title == 'screensaver':
			os.system('gnome-screensaver-preferences &')

		elif title == 'conexiones-red':
			os.system('nm-connection-editor &')
		elif title == 'herramientas-red':
			os.system('gnome-nettool &')
		elif title == 'sitios-red':
			os.system('nautilus --no-desktop network: &')
		elif title == 'proxy':
			os.system('gnome-network-properties &')
		elif title == 'firewall':
			os.system('gufw &')
		elif title == 'compartidos':
			os.system('gnome-file-share-properties &')

		elif title == 'software-manager':
			os.system('tuquito-software-manager &')
		elif title == 'app_fav':
			os.system('gnome-default-applications-properties &')
		elif title == 'clean':
			os.system('tuquito-cleanup &')

		elif title == 'fecha-hora':
			os.system('time-admin &')
		elif title == 'idioma':
			os.system('/usr/bin/gnome-language-selector &')
		elif title == 'boot':
			os.system('su-to-root -X -c /usr/sbin/startupmanager &')
		elif title == 'estado':
			os.system('gnome-system-monitor &')
		elif title == 'garfio':
			os.system('gksu /usr/lib/tuquito/garfio/garfio.py -D "Garfio" &')
		elif title == 'sucesos':
			os.system('gnome-system-log &')
		elif title == 'claves':
			os.system('seahorse &')

		elif title == 'cuentas-usuarios':
			os.system('users-admin &')
		elif title == 'control-parental':
			os.system('tuquito-control-parental &')
		elif title == 'gdm':
			os.system('gdmsetup &')

		elif title == 'hardinfo':
			os.system('hardinfo &')
		elif title == 'impresoras':
			os.system('system-config-printer &')
		elif title == 'discos':
			os.system('palimpsest &')
		elif title == 'controladores':
			os.system('/usr/bin/jockey-gtk &')
		elif title == 'ndiswrapper':
			os.system('gksu /usr/sbin/ndisgtk &')
		elif title == 'teclado':
			os.system('gnome-keyboard-properties &')
		elif title == 'mouse':
			os.system('gnome-mouse-properties &')
		elif title == 'sonido':
			os.system('gnome-volume-control &')
		elif title == 'bluetooth':
			os.system('bluetooth-properties &')
		elif title == 'about':
			os.system('/usr/lib/tuquito/tuquito-control-center/about.py &')

if __name__ == '__main__':
	gtk.gdk.threads_init()
	Center()
	gtk.main()
