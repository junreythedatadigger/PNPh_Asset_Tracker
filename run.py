from app import create_app

app = create_app()

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)  # Set host to 0.0.0.0 to allow access from other devices