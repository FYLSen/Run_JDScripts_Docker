from app import getJDCookie

if __name__ == '__main__':

    app.run(host = 'localhost', port = int(os.environ.get('PORT')))