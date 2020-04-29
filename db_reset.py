from cename import db
from cename.utils import prepare_db
from test import data_generator

if __name__ == "__main__":
    choice = input("Proceed with database complete reset? YES(Y)/NO(N)]: ").lower() 
    if choice == "yes" or choice == "y":
        db.drop_all()
        db.create_all()
        prepare_db()
        print("cleared")
        choice = input("Do you want to generate data in the database?(y/n)").lower()
        if choice == "yes" or choice == 'y':
            data_generator.start()
            print("Generation completed\nClosing...")
    else:
        print("Operation canceled")