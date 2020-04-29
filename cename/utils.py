from cename import db
from cename.models import Region


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