"""Common configuration constants
"""

PROJECTNAME = 'collective.ckeditor'

PROJECTTITLE = 'CKeditor for Plone'

I18NDOMAIN = 'collective.ckeditor'

# the default toolbar used by CKEditor
CKEDITOR_PLONE_DEFAULT_TOOLBAR = """[
    ['Source','-','Templates'],
    ['PasteText','PasteFromWord','SpellChecker'],
    ['Undo'],
    ['Bold','Italic','Underline','Strike'],
    ['NumberedList','BulletedList','-','Outdent','Indent'],
    ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
    ['Link','Unlink','Anchor'],
    ['Image','Table','HorizontalRule','SpecialChar','Maximize'],
    '/',
    ['Style','Format','TextColor','Subscript','Superscript'],
]"""

# quintagroup.com (from qPloneResolveUID product)
RUID_URL_PATTERN = 'resolveuid'
DOCUMENT_DEFAULT_OUTPUT_TYPE = "text/x-html-safe"
REQUIRED_TRANSFORM = "ck_ruid_to_url"
TAG_PATTERN = r'(\<(img|a|embed)[^>]*>)'
UID_PATTERN = r'(?P<uid_url>[^\"\']*%s/(?P<uid>[^\/\"\'#? ]*))' % \
   RUID_URL_PATTERN
