from django.test import TestCase, override_settings
from django.test.client import RequestFactory

import mock
from flags.models import FlaggablePage, FlaggablePageMixin, FlagState


class FlagStateTestCase(TestCase):
    def test_flag_str(self):
        state = FlagState.objects.create(name='MY_FLAG',
                                         condition='boolean',
                                         value='True')
        self.assertEqual(
            str(state), 'MY_FLAG is enabled when boolean is True')


class FlaggablePageMixinTestCase(TestCase):

    def setUp(self):
        self.test_revision = FlaggablePageMixin()
        self.test_revision.feature_flag_name = 'TEST_FLAG'
        self.test_revision.show_draft_with_feature_flag = False

        self.test_page = FlaggablePageMixin()
        self.test_page.get_latest_revision_as_page = mock.Mock()
        self.test_page.get_latest_revision_as_page.return_value = \
            self.test_revision

        self.request = RequestFactory().get('/test')

    @override_settings(FLAGS={'TEST_FLAG': {}})
    @mock.patch('flags.models.Page.serve')
    def test_serve_flaggable_flag_disabled_dont_show_draft(self, mock_serve):
        """ Flag is disabled and show_draft is disabled, pass through to
        Page.serve() """
        self.test_page.serve_flaggable(self.request)
        mock_serve.assert_called_once_with(self.test_page, self.request)

    @override_settings(FLAGS={'TEST_FLAG': {'boolean': True}})
    @mock.patch('flags.models.Page.serve')
    def test_serve_flaggable_flag_enabled_dont_show_draft(self, mock_serve):
        """ Flag is enabled and show_draft is disabled, pass through to
        Page.serve() """
        self.test_page.serve_flaggable(self.request)
        mock_serve.assert_called_once_with(self.test_page, self.request)

    @override_settings(FLAGS={'TEST_FLAG': {'boolean': True}})
    @mock.patch('flags.models.Page.serve')
    def test_serve_flaggable_flag_enabled_show_draft(self, mock_serve):
        """ Flag is enabled and show_draft is enabled, serve latest
        revision """
        self.test_revision.show_draft_with_feature_flag = True
        self.test_page.serve_flaggable(self.request)
        mock_serve.assert_called_once_with(self.test_revision, self.request)

    @mock.patch('flags.models.Page.route')
    def test_route_flaggable_path_components(self, mock_route):
        """ path_components is given, pass through to Page.route() """
        self.test_page.route_flaggable(self.request, ['test'])
        mock_route.assert_called_once_with(self.test_page,
                                           self.request,
                                           ['test'])

    @override_settings(FLAGS={'TEST_FLAG': {}})
    @mock.patch('flags.models.Page.route')
    def test_route_flaggable_flag_disabled_dont_show_draft(self, mock_route):
        """ Flag is disabled and show_draft is disabled, pass through to
        Page.route() """
        self.test_page.route_flaggable(self.request, [])
        mock_route.assert_called_once_with(self.test_page, self.request, [])

    @override_settings(FLAGS={'TEST_FLAG': {'boolean': True}})
    @mock.patch('flags.models.Page.route')
    def test_route_flaggable_flag_enabled_dont_show_draft(self, mock_route):
        """ Flag is enabled and show_draft is disabled, pass through to
        Page.route() """
        self.test_page.route_flaggable(self.request, [])
        mock_route.assert_called_once_with(self.test_page, self.request, [])

    @override_settings(FLAGS={'TEST_FLAG': {'boolean': True}})
    @mock.patch('flags.models.RouteResult')
    def test_route_flaggable_flag_enabled_show_draft(self, mock_routeresult):
        """ Flag is enabled and show_draft is enabled, route the page """
        self.test_revision.show_draft_with_feature_flag = True
        self.test_page.route_flaggable(self.request, [])
        mock_routeresult.assert_called_once_with(self.test_page)


class FlaggablePageTestCase(TestCase):

    def setUp(self):
        self.test_page = FlaggablePage()
        self.request = RequestFactory().get('/test')

    def test_serve(self):
        with mock.patch.object(self.test_page, 'serve_flaggable') \
                as mock_serve_flaggable:
            self.test_page.serve(self.request)
        mock_serve_flaggable.assert_called_with(self.request)

    def test_route(self):
        with mock.patch.object(self.test_page, 'route_flaggable') \
                as mock_route_flaggable:
            self.test_page.route(self.request, [])
        mock_route_flaggable.assert_called_with(self.request, [])
