import flaskr.__init__
app = flaskr.create_app()
app.secret_key = 'super secret key'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
