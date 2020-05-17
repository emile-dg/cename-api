from cename import app, db
import logging

if __name__ == "__main__":
    logging.basicConfig(filename="cename_api.log", 
                        level=logging.DEBUG,
                        filemode='w',
                        format="[%(levelname)s] [%(asctime)s] : %(message)s",
                        datefmt="%d/%m/%Y %I:%M:%S %p")
    logging.debug("Starting server...")
    app.run(debug=False, host="0.0.0.0", port=1909)