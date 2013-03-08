import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.plugins as lib_plugins
import ckan.lib.navl.validators as validators
import ckan.logic.converters as converters


class ExampleIDatasetFormPlugin(plugins.SingletonPlugin,
        lib_plugins.DefaultDatasetForm):
    '''An example IDatasetForm CKAN plugin.

    Uses a tag vocabulary to add a custom metadata field to datasets.

    '''
    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.IDatasetForm, inherit=False)

    # These record how many times methods that this plugin's methods are
    # called, for testing purposes.
    num_times_check_data_dict_called = 0
    num_times_new_template_called = 0
    num_times_comments_template_called = 0
    num_times_search_template_called = 0
    num_times_read_template_called = 0
    num_times_history_template_called = 0
    num_times_package_form_called = 0

    def create_country_codes(self):
        '''Create country_codes vocab and tags, if they don't exist already.

        Note that you could also create the vocab and tags using CKAN's API,
        and once they are created you can edit them (e.g. to add and remove
        possible dataset country code values) using the API.

        '''
        user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
        context = {'user': user['name']}
        try:
            data = {'id': 'country_codes'}
            toolkit.get_action('vocabulary_show')(context, data)
            logging.info("Example genre vocabulary already exists, skipping.")
        except toolkit.ObjectNotFound:
            logging.info("Creating vocab 'country_codes'")
            data = {'name': 'country_codes'}
            vocab = toolkit.get_action('vocabulary_create')(context, data)
            for tag in (u'uk', u'ie', u'de', u'fr', u'es'):
                logging.info(
                        "Adding tag {0} to vocab 'country_codes'".format(tag))
                data = {'name': tag, 'vocabulary_id': vocab['id']}
                toolkit.get_action('tag_create')(context, data)

    def create_language_codes(self):
	user = toolkit.get_action('get_site_user')({'ignore_auth':True},{})
	context = {'user':user['name']}

	try:
            data = {'id': 'language'}
            toolkit.get_action('vocabulary_show')(context, data)
            logging.info("Example genre vocabulary already exists, skipping.")
        except toolkit.ObjectNotFound:
            logging.info("Creating vocab 'language'")
            data = {'name': 'language'}
            vocab = toolkit.get_action('vocabulary_create')(context, data)
            for tag in (u'English', u'Chinese', u'Spanish', u'Swedish', u'French'):
                logging.info(
                        "Adding tag {0} to vocab 'Language'".format(tag))
                data = {'name': tag, 'vocabulary_id': vocab['id']}
                toolkit.get_action('tag_create')(context, data)
    
    def create_datatypes(self):
	user = toolkit.get_action('get_site_user')({'ignore_auth':True},{})
	context = {'user':user['name']}

	try:
            data = {'id': 'datatypes'}
            toolkit.get_action('vocabulary_show')(context, data)
            logging.info("Example genre vocabulary already exists, skipping.")
        except toolkit.ObjectNotFound:
            logging.info("Creating vocab 'filetypes'")
            data = {'name': 'datatypes'}
            vocab = toolkit.get_action('vocabulary_create')(context, data)
            for tag in (u'image', u'documents', u'people'):
                logging.info(
                        "Adding tag {0} to vocab 'filetypes'".format(tag))
                data = {'name': tag, 'vocabulary_id': vocab['id']}
                toolkit.get_action('tag_create')(context, data)
    
    def create_keywords(self):
	user = toolkit.get_action('get_site_user')({'ignore_auth':True},{})
	context = {'user':user['name']}

	try:
            data = {'id': 'keywords'}
            toolkit.get_action('vocabulary_show')(context, data)
            logging.info("Example genre vocabulary already exists, skipping.")
        except toolkit.ObjectNotFound:
            logging.info("Creating vocab 'keywords'")
            data = {'name': 'keywords'}
            vocab = toolkit.get_action('vocabulary_create')(context, data)
            for tag in (u'earthquake', u'diamond', u'gas'):
                logging.info(
                        "Adding tag {0} to vocab 'keywords'".format(tag))
                data = {'name': tag, 'vocabulary_id': vocab['id']}
                toolkit.get_action('tag_create')(context, data)



    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config, 'templates')

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def form_to_db_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).form_to_db_schema()

        # Add our custom country_code metadata field to the schema.
        schema.update({
                'country_code': [validators.ignore_missing,
                    converters.convert_to_tags('country_codes')]
                })

        # Add our custom_test metadata field to the schema, this one will use
        # convert_to_extras instead of convert_to_tags.
        schema.update({
                'custom_text': [validators.ignore_missing,
                    converters.convert_to_extras]
                })
	
	schema.update({
		'language': [validators.ignore_missing,
			converters.convert_to_tags('language')]
		})
	schema.update({
                'datatypes': [validators.ignore_missing,
                    converters.convert_to_tags('datatype')]
                })
	schema.update({
                'keywords': [validators.ignore_missing,
                    converters.convert_to_tags('keywords')]
                })
	
        return schema

    def db_to_form_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).db_to_form_schema()

        # Don't show vocab tags mixed in with normal 'free' tags
        # (e.g. on dataset pages, or on the search page)
        schema['tags']['__extras'].append(converters.free_tags_only)

        # Add our custom country_code metadata field to the schema.
        schema.update({
            'country_code': [
                converters.convert_from_tags('country_codes'),
                validators.ignore_missing]
            })

        # Add our custom_text field to the dataset schema.
        schema.update({
            'custom_text': [
                converters.convert_from_extras, validators.ignore_missing]
            })
	
	schema.update({
		'language': [
		converters.convert_from_tags('language'),
		validators.ignore_missing],
		'datatypes': [
		converters.convert_from_tags('datatypes'),
		validators.ignore_missing],
		'keywords':[
		converters.convert_from_tags('keywords'),
		validators.ignore_missing]
	})
	
        return schema

    def setup_template_variables(self, context, data_dict=None):
        super(ExampleIDatasetFormPlugin, self).setup_template_variables(
                context, data_dict)

        # Create the country_codes vocab and tags, if they don't already exist.
        self.create_country_codes()
	
	# Add customized language
	self.create_language_codes()
	self.create_datatypes()
	self.create_keywords()
        # Add the list of available country codes, from the country_codes
        # vocab, to the template context.
        try:
            toolkit.c.country_codes = toolkit.get_action('tag_list')(
                    context, {'vocabulary_id': 'country_codes'})
        except toolkit.ObjectNotFound:
            toolkit.c.country_codes = None
	
	try:
		toolkit.c.language = toolkit.get_action('tag_list')(
			context,{'vocabulary_id': 'language'})
	except toolkit.ObjectNotFound:
		toolkit.c.language = None
	try:
		toolkit.c.datatypes = toolkit.get_action('tag_list')(
			context,{'vocabulary_id': 'datatypes'})
	except toolkit.ObjectNotFound:
		toolkit.c.datatypes = None
	
	try:
		toolkit.c.keywords = toolkit.get_action('tag_list')(
			context,{'vocabulary_id': 'keywords'})
	except toolkit.ObjectNotFound:
		toolkit.c.keywords = None


    # These methods just record how many times they're called, for testing
    # purposes.
    # TODO: It might be better to test that custom templates returned by
    # these methods are actually used, not just that the methods get
    # called.

    def new_template(self):
        ExampleIDatasetFormPlugin.num_times_new_template_called += 1
        return lib_plugins.DefaultDatasetForm.new_template(self)

    def comments_template(self):
        ExampleIDatasetFormPlugin.num_times_comments_template_called += 1
        return lib_plugins.DefaultDatasetForm.comments_template(self)

    def search_template(self):
        ExampleIDatasetFormPlugin.num_times_search_template_called += 1
        return lib_plugins.DefaultDatasetForm.search_template(self)

    def read_template(self):
        ExampleIDatasetFormPlugin.num_times_read_template_called += 1
        return lib_plugins.DefaultDatasetForm.read_template(self)

    def history_template(self):
        ExampleIDatasetFormPlugin.num_times_history_template_called += 1
        return lib_plugins.DefaultDatasetForm.history_template(self)

    def package_form(self):
        ExampleIDatasetFormPlugin.num_times_package_form_called += 1
        return lib_plugins.DefaultDatasetForm.package_form(self)

    def check_data_dict(self, data_dict, schema=None):
        ExampleIDatasetFormPlugin.num_times_check_data_dict_called += 1
        # Disable DefaultDatasetForm's check_data_dict(), because it breaks
        # with the new three-stage dataset creation when using
        # convert_to_extras.
        #return lib_plugins.DefaultDatasetForm.check_data_dict(self, data_dict,
        #        schema)
