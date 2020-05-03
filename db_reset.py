from cename.models import Region
from cename import db
from test import data_generator


def prepare_db():
    """Prepare the database with necessary entries"""
    regions = {
            'ADA': 'ADAMAWA', 
            'CEN': 'CENTER', 
            'EST': 'EAST', 
            'FND': 'FAR NORTH', 
            'LIT': 'LITORAL',
            'NRD': 'NORD', 
            'NDW': 'NORD WEST', 
            'STH': 'SOUTH', 
            'STW': 'SOUTH WEST', 
            'WST': 'WEST'
        }
    for code in regions.keys():
        db.session.add(Region(region_code=code, region_name=regions[code]))
    db.session.commit()

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