from app import create_app, config

app = create_app(config_name="prod")

if __name__ == "__main__":
    app.run()