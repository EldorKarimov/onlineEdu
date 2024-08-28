def file_checker(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'png', 'jpg'}
    return '.' in filename and filename.split('.')[1].lower() in ALLOWED_EXTENSIONS