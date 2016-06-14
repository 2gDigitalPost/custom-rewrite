import unittest
import os
import time

from ConfigParser import SafeConfigParser

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select


class ElementEvalTest(unittest.TestCase):
    def setUp(self):
        parser = SafeConfigParser()
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        parser.read(config_path + '/config.ini')

        binary = FirefoxBinary(parser.get('webdriver', 'firefox_binary'))

        self.browser = webdriver.Firefox(firefox_binary=binary)

        self.target_website = parser.get('url', 'test')

        username = parser.get('login', 'username')
        password = parser.get('login', 'password')

        self.login(username, password)

    def tearDown(self):
        self.browser.quit()

    def login(self, username, password):
        self.browser.get(self.target_website)

        username_field = self.browser.find_element_by_name('login')
        password_field = self.browser.find_element_by_name('password')
        submit_field = self.browser.find_element_by_name('Submit')

        username_field.send_keys(username)
        password_field.send_keys(password)

        submit_field.submit()

    def load_element_eval_page(self):
        self.browser.get(self.target_website)

        time.sleep(3)

        element_eval_link = self.browser.find_element_by_xpath('//div[@spt_title="Report"]')
        element_eval_link.click()

        time.sleep(2)

    def test_load_element_eval_page(self):
        self.load_element_eval_page()

        element_eval_header = self.browser.find_element_by_class_name('spt_tab_header_label')
        self.assertEqual('Report', element_eval_header.text)

    def test_reload_page_keeps_input_values(self):
        self.load_element_eval_page()

        # Some values to pass into the input widgets
        operator_field_input = 'Test Operator'
        title_field_input = 'Test Title'
        season_field_input = 'Test Season'
        episode_field_input = 'Test Episode'
        version_field_input = 'Test Version'
        po_number_field_input = 'Test PO Number'
        file_name_field_input = 'Test File Name'
        roll_up_blank_field_input = 'Test Roll Up Blank'
        bars_tone_field_input = 'Test Bars/Tone'
        black_silence_1_field_input = 'Test Black/Silence (1)'
        slate_silence_field_input = 'Test Slate/Silence'
        black_silence_2_field_input = 'Test Black/Silence (2)'
        start_of_program_field_input = 'Test Start of Program'
        end_of_program_field_input = 'Test End of Program'
        active_video_begins_field_input = 'Test Active Video Begins'
        active_video_ends_field_input = 'Test Active Video Ends'
        horizontal_blanking_field_input = 'Test Horizontal Blanking'
        luminance_peak_field_input = 'Test Luminance Peak'
        chroma_peak_field_input = 'Test Chroma Peak'
        head_logo_field_input = 'Test Head Logo'
        tail_logo_field_input = 'Test Tail Logo'
        total_runtime_field_input = 'Test Total Runtime'
        tv_feature_trailer_field_input = 'Test TV/Feature/Trailer'
        textless_tail_field_input = 'Test Textless @ Tail'
        notices_field_input = 'Test Notices'
        language_field_input = 'Test Language'
        cc_subtitles_field_input = 'Test CC/Subtitles'
        vitc_field_input = 'Test VITC'
        source_barcode_field_input = 'Test Source Barcode'
        element_qc_barcode_field_input = 'Test Element QC Barcode'

        # Send the input values to all the input widgets on the page
        self.browser.find_element_by_name('operator').send_keys(operator_field_input)
        self.browser.find_element_by_name('title_data').send_keys(title_field_input)
        self.browser.find_element_by_name('season').send_keys(season_field_input)
        self.browser.find_element_by_name('episode').send_keys(episode_field_input)
        self.browser.find_element_by_name('version').send_keys(version_field_input)
        self.browser.find_element_by_name('po_number').send_keys(po_number_field_input)
        self.browser.find_element_by_name('file_name').send_keys(file_name_field_input)
        self.browser.find_element_by_name('roll_up_blank').send_keys(roll_up_blank_field_input)
        self.browser.find_element_by_name('bars_tone').send_keys(bars_tone_field_input)
        self.browser.find_element_by_name('black_silence_1').send_keys(black_silence_1_field_input)
        self.browser.find_element_by_name('slate_silence').send_keys(slate_silence_field_input)
        self.browser.find_element_by_name('black_silence_2').send_keys(black_silence_2_field_input)
        self.browser.find_element_by_name('start_of_program').send_keys(start_of_program_field_input)
        self.browser.find_element_by_name('end_of_program').send_keys(end_of_program_field_input)
        self.browser.find_element_by_name('active_video_begins').send_keys(active_video_begins_field_input)
        self.browser.find_element_by_name('active_video_ends').send_keys(active_video_ends_field_input)
        self.browser.find_element_by_name('horizontal_blanking').send_keys(horizontal_blanking_field_input)
        self.browser.find_element_by_name('luminance_peak').send_keys(luminance_peak_field_input)
        self.browser.find_element_by_name('chroma_peak').send_keys(chroma_peak_field_input)
        self.browser.find_element_by_name('head_logo').send_keys(head_logo_field_input)
        self.browser.find_element_by_name('tail_logo').send_keys(tail_logo_field_input)
        self.browser.find_element_by_name('total_runtime').send_keys(total_runtime_field_input)
        self.browser.find_element_by_name('tv_feature_trailer').send_keys(tv_feature_trailer_field_input)
        self.browser.find_element_by_name('textless_tail').send_keys(textless_tail_field_input)
        self.browser.find_element_by_name('notices').send_keys(notices_field_input)
        self.browser.find_element_by_name('language').send_keys(language_field_input)
        self.browser.find_element_by_name('cc_subtitles').send_keys(cc_subtitles_field_input)
        self.browser.find_element_by_name('vitc').send_keys(vitc_field_input)
        self.browser.find_element_by_name('source_barcode').send_keys(source_barcode_field_input)
        self.browser.find_element_by_name('element_qc_barcode').send_keys(element_qc_barcode_field_input)

        # Also select values for all the select widgets
        style_select_option = 'Technical'
        style_select = Select(self.browser.find_element_by_id('style'))
        style_select.select_by_visible_text(style_select_option)

        bay_select_option = 'Bay 3'
        bay_select = Select(self.browser.find_element_by_id('bay'))
        bay_select.select_by_visible_text(bay_select_option)

        machine_select_option = 'VTR233'
        machine_select = Select(self.browser.find_element_by_id('machine_number'))
        machine_select.select_by_visible_text(machine_select_option)

        format_select_option = 'File - WAV'
        format_select = Select(self.browser.find_element_by_id('format'))
        format_select.select_by_visible_text(format_select_option)

        standard_select_option = 'PAL'
        standard_select = Select(self.browser.find_element_by_id('standard'))
        standard_select.select_by_visible_text(standard_select_option)

        frame_rate_select_option = '24p'
        frame_rate_select = Select(self.browser.find_element_by_id('frame_rate'))
        frame_rate_select.select_by_visible_text(frame_rate_select_option)

        video_aspect_ratio_select_option = '4x3 2.35 Letterbox'
        video_aspect_ratio_select = Select(self.browser.find_element_by_id('video_aspect_ratio'))
        video_aspect_ratio_select.select_by_visible_text(video_aspect_ratio_select_option)

        label_select_option = 'Fair'
        label_select = Select(self.browser.find_element_by_id('label'))
        label_select.select_by_visible_text(label_select_option)

        # Find the button that refreshes the page (the add row button in this case) and click it
        add_row_button = self.browser.find_element_by_class_name('add_row_button')
        add_row_button.click()

        # Give the page a few seconds to reload
        time.sleep(2)

        # Now check all the input values, and make sure they're the same as what was put in before
        self.assertEqual(operator_field_input, self.browser.find_element_by_name('operator').get_attribute('value'))
        self.assertEqual(title_field_input, self.browser.find_element_by_name('title_data').get_attribute('value'))
        self.assertEqual(season_field_input, self.browser.find_element_by_name('season').get_attribute('value'))
        self.assertEqual(episode_field_input, self.browser.find_element_by_name('episode').get_attribute('value'))
        self.assertEqual(version_field_input, self.browser.find_element_by_name('version').get_attribute('value'))
        self.assertEqual(po_number_field_input, self.browser.find_element_by_name('po_number').get_attribute('value'))
        self.assertEqual(file_name_field_input, self.browser.find_element_by_name('file_name').get_attribute('value'))
        self.assertEqual(roll_up_blank_field_input,
                         self.browser.find_element_by_name('roll_up_blank').get_attribute('value'))
        self.assertEqual(bars_tone_field_input, self.browser.find_element_by_name('bars_tone').get_attribute('value'))
        self.assertEqual(black_silence_1_field_input,
                         self.browser.find_element_by_name('black_silence_1').get_attribute('value'))
        self.assertEqual(slate_silence_field_input,
                         self.browser.find_element_by_name('slate_silence').get_attribute('value'))
        self.assertEqual(black_silence_2_field_input,
                         self.browser.find_element_by_name('black_silence_2').get_attribute('value'))
        self.assertEqual(start_of_program_field_input,
                         self.browser.find_element_by_name('start_of_program').get_attribute('value'))
        self.assertEqual(end_of_program_field_input,
                         self.browser.find_element_by_name('end_of_program').get_attribute('value'))
        self.assertEqual(active_video_begins_field_input,
                         self.browser.find_element_by_name('active_video_begins').get_attribute('value'))
        self.assertEqual(active_video_ends_field_input,
                         self.browser.find_element_by_name('active_video_ends').get_attribute('value'))
        self.assertEqual(horizontal_blanking_field_input,
                         self.browser.find_element_by_name('horizontal_blanking').get_attribute('value'))
        self.assertEqual(luminance_peak_field_input,
                         self.browser.find_element_by_name('luminance_peak').get_attribute('value'))
        self.assertEqual(chroma_peak_field_input,
                         self.browser.find_element_by_name('chroma_peak').get_attribute('value'))
        self.assertEqual(head_logo_field_input, self.browser.find_element_by_name('head_logo').get_attribute('value'))
        self.assertEqual(tail_logo_field_input, self.browser.find_element_by_name('tail_logo').get_attribute('value'))
        self.assertEqual(total_runtime_field_input,
                         self.browser.find_element_by_name('total_runtime').get_attribute('value'))
        self.assertEqual(tv_feature_trailer_field_input,
                         self.browser.find_element_by_name('tv_feature_trailer').get_attribute('value'))
        self.assertEqual(textless_tail_field_input,
                         self.browser.find_element_by_name('textless_tail').get_attribute('value'))
        self.assertEqual(notices_field_input, self.browser.find_element_by_name('notices').get_attribute('value'))
        self.assertEqual(language_field_input, self.browser.find_element_by_name('language').get_attribute('value'))
        self.assertEqual(cc_subtitles_field_input,
                         self.browser.find_element_by_name('cc_subtitles').get_attribute('value'))
        self.assertEqual(vitc_field_input, self.browser.find_element_by_name('vitc').get_attribute('value'))
        self.assertEqual(source_barcode_field_input,
                         self.browser.find_element_by_name('source_barcode').get_attribute('value'))
        self.assertEqual(element_qc_barcode_field_input,
                         self.browser.find_element_by_name('element_qc_barcode').get_attribute('value'))

        # Also check the select widgets and make sure they are what was selected
        style_select = Select(self.browser.find_element_by_id('style'))
        bay_select = Select(self.browser.find_element_by_id('bay'))
        machine_select = Select(self.browser.find_element_by_id('machine_number'))
        format_select = Select(self.browser.find_element_by_id('format'))
        standard_select = Select(self.browser.find_element_by_id('standard'))
        frame_rate_select = Select(self.browser.find_element_by_id('frame_rate'))
        video_aspect_ratio_select = Select(self.browser.find_element_by_id('video_aspect_ratio'))
        label_select = Select(self.browser.find_element_by_id('label'))

        self.assertEqual(style_select_option, style_select.first_selected_option.text)
        self.assertEqual(bay_select_option, bay_select.first_selected_option.text)
        self.assertEqual(machine_select_option, machine_select.first_selected_option.text)
        self.assertEqual(format_select_option, format_select.first_selected_option.text)
        self.assertEqual(standard_select_option, standard_select.first_selected_option.text)
        self.assertEqual(frame_rate_select_option, frame_rate_select.first_selected_option.text)
        self.assertEqual(video_aspect_ratio_select_option, video_aspect_ratio_select.first_selected_option.text)
        self.assertEqual(label_select_option, label_select.first_selected_option.text)

    def test_add_and_remove_row_buttons(self):
        self.load_element_eval_page()

        # Get the number of rows currently on the audio config table
        # Two rows are dedicated to the table headers, so don't count those
        original_row_count = len(
            self.browser.find_elements_by_xpath("//table[@id='audio_configuration_table']/tbody/tr")) - 2

        # Start with the add row button
        add_row_button = self.browser.find_element_by_class_name('add_row_button')
        add_row_button.click()

        # Give the page a few seconds to reload
        time.sleep(2)

        # Count the new number of rows, and assert that it's one more than we had
        new_row_count = len(
            self.browser.find_elements_by_xpath("//table[@id='audio_configuration_table']/tbody/tr")) - 2
        self.assertEqual(original_row_count + 1, new_row_count)

        # Now the subtract button
        subtract_row_button = self.browser.find_element_by_class_name('subtract_row_button')
        subtract_row_button.click()

        # Give the page a few seconds to reload
        time.sleep(2)

        # Count the new number of rows, and assert that it's one less than we had (back to the original count)
        new_row_count = len(
            self.browser.find_elements_by_xpath("//table[@id='audio_configuration_table']/tbody/tr")) - 2
        self.assertEqual(original_row_count, new_row_count)

    def test_cannot_remove_all_audio_config_rows(self):
        self.load_element_eval_page()

        # Get the number of rows currently on the audio config table
        # Two rows are dedicated to the table headers, so don't count those
        original_row_count = len(
            self.browser.find_elements_by_xpath("//table[@id='audio_configuration_table']/tbody/tr")) - 2

        # Iterate down from the row count to one
        for x in range(original_row_count, 1, -1):
            # Click the subtract button
            subtract_row_button = self.browser.find_element_by_class_name('subtract_row_button')
            subtract_row_button.click()

            # Give the page a few seconds to reload
            time.sleep(2)

        # Make sure the button is not visible
        try:
            self.browser.find_element_by_class_name('subtract_row_button')
            subtract_button_is_visible = True
        except NoSuchElementException:
            subtract_button_is_visible = False

        self.assertFalse(subtract_button_is_visible)

        # Now check if the subtract button is added back when another row is added. Start by adding a row.
        add_row_button = self.browser.find_element_by_class_name('add_row_button')
        add_row_button.click()

        time.sleep(2)

        # Make sure the button is visible
        try:
            self.browser.find_element_by_class_name('subtract_row_button')
            subtract_button_is_visible = True
        except NoSuchElementException:
            subtract_button_is_visible = False

        self.assertTrue(subtract_button_is_visible)

    def test_reload_page_keeps_audio_config_values(self):
        self.load_element_eval_page()

        # Get the number of rows currently on the audio config table
        # Two rows are dedicated to the table headers, so don't count those
        original_row_count = len(
            self.browser.find_elements_by_xpath("//table[@id='audio_configuration_table']/tbody/tr")) - 2

        # Input test values in the boxes
        for row in range(original_row_count):
            channel_text = 'Channel {0}'.format(row)
            content_text = 'Content {0}'.format(row)
            tone_text = 'Tone {0}'.format(row)
            peak_text = 'Peak {0}'.format(row)

            channel_input = self.browser.find_element_by_name('channel-{0}'.format(row))
            content_input = self.browser.find_element_by_name('content-{0}'.format(row))
            tone_input = self.browser.find_element_by_name('tone-{0}'.format(row))
            peak_input = self.browser.find_element_by_name('peak-{0}'.format(row))

            channel_input.send_keys(channel_text)
            content_input.send_keys(content_text)
            tone_input.send_keys(tone_text)
            peak_input.send_keys(peak_text)

        # Click the add row button
        self.browser.find_element_by_class_name('add_row_button').click()

        time.sleep(2)

        # Check if the text inputs still have their values (the last row won't have anything)
        for row in range(original_row_count):
            channel_text = 'Channel {0}'.format(row)
            content_text = 'Content {0}'.format(row)
            tone_text = 'Tone {0}'.format(row)
            peak_text = 'Peak {0}'.format(row)

            self.assertEqual(channel_text, self.browser.find_element_by_name(
                'channel-{0}'.format(row)).get_attribute('value'))
            self.assertEqual(content_text, self.browser.find_element_by_name(
                'content-{0}'.format(row)).get_attribute('value'))
            self.assertEqual(tone_text, self.browser.find_element_by_name(
                'tone-{0}'.format(row)).get_attribute('value'))
            self.assertEqual(peak_text, self.browser.find_element_by_name(
                'peak-{0}'.format(row)).get_attribute('value'))

        # Make sure the added row's values are blank, and not "None"
        self.assertEqual('',
                         self.browser.find_element_by_name('channel-{0}'.format(original_row_count)).get_attribute(
                             'value'))
        self.assertEqual('',
                         self.browser.find_element_by_name('content-{0}'.format(original_row_count)).get_attribute(
                             'value'))
        self.assertEqual('',
                         self.browser.find_element_by_name('tone-{0}'.format(original_row_count)).get_attribute(
                             'value'))
        self.assertEqual('',
                         self.browser.find_element_by_name('peak-{0}'.format(original_row_count)).get_attribute(
                             'value'))

        # Now verify that when a row is removed, it's original contents are removed as well.
        # Start by removing two rows
        self.browser.find_element_by_class_name('subtract_row_button').click()
        time.sleep(2)
        self.browser.find_element_by_class_name('subtract_row_button').click()
        time.sleep(2)

        # Add a row back in
        self.browser.find_element_by_class_name('add_row_button').click()
        time.sleep(2)

        # Now verify the last row is empty
        last_row_index = len(
            self.browser.find_elements_by_xpath("//table[@id='audio_configuration_table']/tbody/tr")) - 3

        self.assertEqual('',
                         self.browser.find_element_by_name('channel-{0}'.format(last_row_index)).get_attribute('value'))
        self.assertEqual('',
                         self.browser.find_element_by_name('content-{0}'.format(last_row_index)).get_attribute('value'))
        self.assertEqual('',
                         self.browser.find_element_by_name('tone-{0}'.format(last_row_index)).get_attribute('value'))
        self.assertEqual('',
                         self.browser.find_element_by_name('peak-{0}'.format(last_row_index)).get_attribute('value'))


if __name__ == '__main__':
    unittest.main()
