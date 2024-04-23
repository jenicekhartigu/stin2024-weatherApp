from website import create_app

# app = create_app()

if __name__ == '__main__':
    # app.run(debug = True)
    
    create_app = create_app()
    create_app.run()
    
else:
    gunicorn_app = create_app()

    
    