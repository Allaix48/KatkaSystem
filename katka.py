# -*- coding: utf-8 -*-


from application import app

if __name__ == "__main__":
    app.run(threaded=True, port=5000)