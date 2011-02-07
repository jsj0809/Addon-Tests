#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): David Burns
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****


from selenium import selenium
from vars import ConnectionParameters
import unittest2 as unittest
import re
from addons_site import DiscoveryPane
from addons_site import AddonsHomePage
import sys
import urllib2

class DiscoveryPaneTests(unittest.TestCase):
    """ This only works with Firefox 4 """    

    baseurl = 'https://services.addons.mozilla.org'
    basepath= '/en-US/firefox/discovery/pane/4.0b10/Darwin' #Need to get this info before run

    @classmethod
    def setUpClass(self):
        urllib2.urlopen(self.baseurl + self.basepath)

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, 
                                ConnectionParameters.port,
                                ConnectionParameters.browser, 
                                self.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_that_users_with_less_than_3_addons_get_what_are_addons(self):
        """ Test case for litmus 15063 - 
        Since Selenium starts with a clean profile all the time this will always have
        less than 3 addons
        """
        discovery_pane = DiscoveryPane(self.selenium, self.basepath)
        what_are_addons_expected = "Add-ons are applications that let you personalize "  
        what_are_addons_expected += "Firefox with extra functionality or style. Try a time-saving" 
        what_are_addons_expected += " sidebar, a weather notifier, or a themed look to make "
        what_are_addons_expected += "Firefox your own. Learn More"

        self.assertEquals(what_are_addons_expected, discovery_pane.what_are_addons_text)

    def test_that_mission_statement_is_on_addons_home_page(self):
        """ TestCase for Litmus 15065 """
        discovery_pane = DiscoveryPane(self.selenium, self.basepath)

        self.assertTrue(discovery_pane.is_element_present(discovery_pane.mission_section))
        expected_text = "Thanks for using Firefox and supporting Mozilla's mission!"
        mission_text = discovery_pane.mission_section_text
        self.assertTrue(expected_text in mission_text)
        self.assertTrue(discovery_pane.is_element_present(discovery_pane.mozilla_org_link))
        download_count_regex = "Add-ons downloaded: (.+)"
        self.assertTrue(re.search(download_count_regex, discovery_pane.download_count_text) != None)
        
    def test_that_addons_count_are_equal_between_amo_and_discovert(self):
        """ TestCase for Litmus 15066 """
        self.skipTest("The counts are not equal causing test to fail")
        amo_home_page = AddonsHomePage(self.selenium)
        amo_download_count = amo_home_page.download_count.replace(",","")

        discovery_pane = DiscoveryPane(self.selenium, self.basepath)
        discovery_download_count_text = discovery_pane.download_count_text
        download_count = re.search("Add-ons downloaded: (.+)", discovery_download_count_text).group(1)
        download_count = download_count.replace(",","")
        self.assertEquals(amo_download_count, download_count)