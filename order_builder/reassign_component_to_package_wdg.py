from tactic.ui.common import BaseRefreshWdg

from pyasm.search import Search
from pyasm.web import DivWdg
from pyasm.widget import SelectWdg, SubmitWdg


class ReassignComponentToPackage(BaseRefreshWdg):
    def init(self):
        self.component_sobject = self.get_sobject_from_kwargs()
        self.package_sobject = self.component_sobject.get_parent()
        self.order_sobject = self.package_sobject.get_parent()

    def get_packages(self):
        """
        Get a list of Packages (sobjects) belonging to the Order that this component belongs to

        :return: List of package sobjects
        """

        # Search for packages, using the parent Order to filter
        package_search = Search('twog/package')
        package_search.add_parent_filter(self.order_sobject)
        packages = package_search.get_sobjects()

        # Filter out the package that the component already belongs to
        packages = [package for package in packages if package.get_code() != self.package_sobject.get_code()]

        # Return a list of packages
        return packages

    def get_package_select_wdg(self):
        """
        Get a SelectWdg that contains all the possible packages that the component can switch to.

        :return: SelectWdg
        """

        # Set up a basic select widget with an empty object
        package_select_wdg = SelectWdg('reassign_package_select')
        package_select_wdg.set_id('reassign_package_select')
        package_select_wdg.add_style('width', '300px')
        package_select_wdg.add_empty_option()

        # Get the packages
        packages = self.get_packages()

        # Add the package names as the labels and the codes as the values
        for package in packages:
            package_select_wdg.append_option(package.get_value('name'), package.get_code())

        # Return the SelectWdg
        return package_select_wdg

    def get_display(self):
        outer_div = DivWdg()
        outer_div.set_id('reassign-component-to-package')

        outer_div.add('This component currently belongs to this package:\n{0}\n'.format(
            self.package_sobject.get('name')))

        package_select_wdg = self.get_package_select_wdg()
        outer_div.add(package_select_wdg)

        submit_button = SubmitWdg('Submit')
        submit_button.add_behavior(self.get_submit_button_behavior(self.component_sobject.get_code()))

        outer_div.add(submit_button)

        return outer_div

    @staticmethod
    def get_submit_button_behavior(component_code):
        behavior = {
            'css_class': 'clickme',
            'type': 'click_up',
            'cbjs_action': '''
try {
    // Get the server object
    var server = TacticServerStub.get();
    var containing_element = bvr.src_el.getParent("#reassign-component-to-package");
    var values = spt.api.get_input_values(containing_element, null, false);

    // Get the form values
    var component_code = '%s';
    var package_code = values.reassign_package_select;

    // Build a search key using the component's code
    var search_key = server.build_search_key('twog/component', component_code, 'twog');

    // Set up the kwargs to update the component data
    var kwargs = {
        'package_code': package_code,
    }

    // Send the update to the server
    server.update(search_key, kwargs);
}
catch(err) {
    spt.app_busy.hide();
    spt.alert(spt.exception.handler(err));
}''' % (component_code)
        }

        return behavior
